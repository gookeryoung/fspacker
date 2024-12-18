import logging
import pathlib
import time
import typing
import pkginfo
import stdlib_list

from fspacker.common import LibraryInfo
from fspacker.config import LIBS_REPO_DIR, PYTHON_VER_SHORT, LIBNAME_MAPPER
from fspacker.utils.performance import perf_tracker

__libs_repo: typing.Dict[str, LibraryInfo] = {}
__builtin_lib_repo: typing.Set[str] = set()

__all__ = [
    "get_libs_repo",
    "update_libs_repo",
    "get_builtin_lib_repo",
    "map_libname",
]


@perf_tracker
def get_libs_repo() -> typing.Dict[str, LibraryInfo]:
    global __libs_repo

    if not len(__libs_repo):
        lib_files = list(
            _
            for _ in LIBS_REPO_DIR.rglob("*")
            if _.suffix in (".whl", ".tar.gz")
        )
        for lib_file in lib_files:
            info = LibraryInfo.from_filepath(lib_file)
            __libs_repo.setdefault(info.meta_data.name, info)
        logging.info(f"Fetching local library, total: [{len(lib_files)}]")

    return __libs_repo


@perf_tracker
def update_libs_repo(lib: str, filepath: pathlib.Path) -> None:
    libs_repo = get_libs_repo()
    libs_repo[lib] = LibraryInfo.from_filepath(filepath)
    logging.info(f"Update libs repo: {libs_repo[lib]}")


@perf_tracker
def get_builtin_lib_repo() -> typing.Set[str]:
    """Analyse and return names of built-in libraries"""

    global __builtin_lib_repo

    if not len(__builtin_lib_repo):
        __builtin_lib_repo = set(stdlib_list.stdlib_list(PYTHON_VER_SHORT))
        logging.info(f"Parse built-in libs: total=[{len(__builtin_lib_repo)}]")

    return __builtin_lib_repo


def map_libname(libname: str) -> str:
    if libname in LIBNAME_MAPPER:
        return LIBNAME_MAPPER[libname].replace("-", "_")
    else:
        libs_repo = get_libs_repo()
        if libname in libs_repo:
            return libname
        return libname.replace("-", "_").replace(".", "_")
