import logging
import pathlib
import subprocess
import typing
import zipfile

import rtoml

from fspacker.common import BuildTarget, LibraryInfo, DependsInfo
from fspacker.config import IGNORE_SYMBOLS, LIBS_REPO_DIR, DEPENDS_FILEPATH
from fspacker.packer.base import BasePacker

__all__ = [
    "LibraryPacker",
]


class LibraryPacker(BasePacker):
    LIBS_REPO: typing.Dict[str, LibraryInfo] = {}
    DEPEND_TREE_REPO: typing.Dict[str, DependsInfo] = {}

    def __init__(self):
        super().__init__()

        self._parse_depends_repo()
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
                filepath = self._download_lib(libname)
                logging.info(f"下载依赖库[{libname}]->[{LIBS_REPO_DIR}]")
                self.LIBS_REPO[libname] = LibraryInfo.from_path(filepath)

            logging.info(f"解压依赖库[{libname}]->[{packages_dir}]")
            self._unzip_lib(libname, packages_dir)

    @staticmethod
    def _download_lib(libname: str) -> pathlib.Path:
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
        lib_filepath = list(_ for _ in LIBS_REPO_DIR.rglob(f"{libname}*"))[0]
        return lib_filepath

    def _unzip_lib(self, lib: str, output_dir):
        """从库文件中解压指定的文件并将其放到特定目录中。"""
        lib_info = self.LIBS_REPO.get(lib)
        dependency = self.DEPEND_TREE_REPO.get(lib)

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
                info = LibraryInfo.from_path(lib_file)
                self.LIBS_REPO.setdefault(info.package_name.lower(), info)

                if len(info.version) > 1:
                    logging.info(
                        f"库文件[{lib_file.stem}]包含多个版本: [{info.version}]"
                    )

            except ValueError as e:
                logging.error(f"分析库文件[{lib_file.stem}]出错, 信息: [{e}]")

    def _parse_depends_repo(self) -> typing.Dict[str, DependsInfo]:
        depends: typing.Dict[str, DependsInfo] = {}
        config = rtoml.load(DEPENDS_FILEPATH)
        for k, v in config.items():
            depends.setdefault(
                k.lower(),
                DependsInfo(
                    name=k,
                    files=config[k].get("files"),
                    folders=config[k].get("folders"),
                    depends=config[k].get("depends"),
                ),
            )
        self.DEPEND_TREE_REPO.update(depends)
        logging.info(f"获取依赖信息: {depends}")
