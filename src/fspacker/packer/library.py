import logging
import subprocess
import typing
import zipfile

from fspacker.common import BuildTarget, LibraryInfo
from fspacker.config import IGNORE_SYMBOLS, LIBS_REPO_DIR
from fspacker.packer.base import BasePacker
from fspacker.packer.depends import parse_depends_tree

__all__ = [
    "LibraryPacker",
]


class LibraryPacker(BasePacker):
    LIBS_REPO: typing.Dict[str, LibraryInfo] = {}

    def __init__(self):
        super().__init__()

        self._parse_libs_repo()

    def pack(self, target: BuildTarget):
        packages_dir = target.packages_dir

        if not packages_dir.exists():
            logging.info(f"创建包目录[{packages_dir}]")
            packages_dir.mkdir(parents=True)

        for libname in target.ast:
            exist_folders = list(
                _.stem for _ in packages_dir.iterdir() if _.is_dir()
            )
            if libname in exist_folders:
                logging.info(
                    f"目录[{packages_dir.name}]下已存在[{libname}]库, 跳过"
                )
                continue

            if libname not in self.LIBS_REPO:
                logging.info(f"库目录中未找到[{libname}]")
                self._download_lib(libname)
                logging.info(f"下载依赖库[{libname}]->[{LIBS_REPO_DIR}]")

            logging.info(f"解压依赖库[{libname}]->[{packages_dir}]")
            self._unzip_lib(libname, packages_dir)

    @staticmethod
    def _download_lib(libname: str):
        subprocess.call(
            [
                "python",
                "-m",
                "pip",
                "download",
                libname,
                "--no-deps",
                "-d",
                str(LIBS_REPO_DIR),
            ],
        )

    def _unzip_lib(self, lib: str, output_dir):
        """从库文件中解压指定的文件并将其放到特定目录中。"""
        dep_tree = parse_depends_tree()
        lib_info = self.LIBS_REPO.get(lib)
        dependency = dep_tree.get(lib)

        if lib_info is not None:
            with zipfile.ZipFile(lib_info.filepath, "r") as f:
                for target_file in f.namelist():
                    if dependency is not None and hasattr(dependency, "files"):
                        relative_path = target_file.replace(
                            f"{lib_info.package_name}/", ""
                        )
                        if relative_path not in dependency.files:
                            continue

                    if any(_ in target_file for _ in IGNORE_SYMBOLS):
                        continue

                    f.extract(target_file, output_dir)

        if dependency is not None and hasattr(dependency, "depends"):
            for depend in dependency.depends:
                if self.LIBS_REPO.get(depend) is None:
                    self._download_lib(depend)
                    logging.info(f"下载依赖库[{depend}]->[{LIBS_REPO_DIR}]")
                self._unzip_lib(depend, output_dir)

    def _parse_libs_repo(self) -> None:
        lib_files = list(
            _
            for _ in LIBS_REPO_DIR.rglob("*")
            if _.suffix in (".whl", ".tar.gz")
        )
        logging.info(f"获取库文件, 总数: {len(lib_files)}")
        for lib_file in lib_files:
            try:
                package_name, *version, build_tag, abi_tag, platform_tag = (
                    lib_file.stem.split("-")
                )
                self.LIBS_REPO.setdefault(
                    package_name.lower(),
                    LibraryInfo(
                        package_name=package_name,
                        version=version,
                        build_tag=build_tag,
                        abi_tag=abi_tag,
                        platform_tag=platform_tag,
                        filepath=lib_file,
                    ),
                )

                if len(version) > 1:
                    logging.info(
                        f"库文件[{lib_file.stem}]包含多个版本: [{version}]"
                    )

            except ValueError as e:
                logging.error(f"分析库文件[{lib_file.stem}]出错, 信息: [{e}]")