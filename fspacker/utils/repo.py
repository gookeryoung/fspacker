import logging
import typing

from fspacker.common import LibraryInfo
from fspacker.config import LIBS_REPO_DIR

__libs_repo: typing.Dict[str, LibraryInfo] = {}


__all__ = [
    "get_libs_repo",
]


def get_libs_repo() -> typing.Dict[str, LibraryInfo]:
    global __libs_repo

    if not len(__libs_repo):
        lib_files = list(_ for _ in LIBS_REPO_DIR.rglob("*") if _.suffix in (".whl", ".tar.gz"))
        logging.info(f"获取库文件, 总数: {len(lib_files)}")
        for lib_file in lib_files:
            try:
                info = LibraryInfo.from_path(lib_file)
                __libs_repo.setdefault(info.package_name.lower(), info)

                if len(info.version) > 1:
                    logging.info(f"库文件[{lib_file.stem}]包含多个版本: [{info.version}]")

            except ValueError as e:
                logging.error(f"分析库文件[{lib_file.stem}]出错, 信息: [{e}]")

    return __libs_repo
