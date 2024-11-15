import logging
import shutil
import typing
import zipfile

import rtoml

from fspacker.common import BuildTarget, LibraryInfo, DependsInfo
from fspacker.config import LIBS_REPO_DIR, DEPENDS_FILEPATH, IGNORE_SYMBOLS
from fspacker.packer.base import BasePacker
from fspacker.utils.wheel import download_install_wheel, download_wheel

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
                _.stem.lower() for _ in packages_dir.iterdir() if _.is_dir()
            )
            if libname in exist_folders:
                logging.info(
                    f"目录[{packages_dir.name}]下已存在[{libname}]库, 跳过"
                )
                continue

            if not self.LIBS_REPO.get(libname):
                filepath = download_wheel(libname)
                if filepath:
                    self.LIBS_REPO[libname] = LibraryInfo.from_path(filepath)
            if self.DEPEND_TREE_REPO.get(libname):
                self.unzip(libname, target)
            else:
                download_install_wheel(libname, target.packages_dir)

    def unzip(self, libname, target):
        dep = self.DEPEND_TREE_REPO.get(libname)
        info = self.LIBS_REPO.get(libname)

        if libname == "PIL":
            filepath = self.LIBS_REPO.get("pillow").filepath
        elif libname == "dateutil":
            filepath = self.LIBS_REPO.get("pillow").filepath
        else:
            filepath = info.filepath if info else None

        if hasattr(dep, "files"):
            with zipfile.ZipFile(info.filepath, "r") as f:
                for target_file in f.namelist():
                    relative_path = target_file.replace(
                        f"{info.package_name}/", ""
                    )
                    if len(dep.files) and relative_path not in dep.files:
                        continue

                    if any(_ in target_file for _ in IGNORE_SYMBOLS):
                        continue

                    f.extract(target_file, target.packages_dir)
        else:
            if filepath:
                shutil.unpack_archive(filepath, target.packages_dir, "zip")

        if hasattr(dep, "depends"):
            for d in dep.depends:
                self.unzip(d, target)

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
                    files=config[k].setdefault("files", []),
                    folders=config[k].setdefault("folders", []),
                    depends=config[k].setdefault("depends", []),
                ),
            )
        self.DEPEND_TREE_REPO.update(depends)
        logging.info(f"获取依赖信息: {depends}")
