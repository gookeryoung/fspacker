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
        logging.info(f"Fetching local library, total: [{len(lib_files)}]")
        for lib_file in lib_files:
            try:
                info = LibraryInfo.from_path(lib_file)
                __libs_repo.setdefault(info.package_name.lower(), info)

            except ValueError as e:
                logging.error(f"Parsing [{lib_file.stem}] error, message: [{e}]")

    return __libs_repo
