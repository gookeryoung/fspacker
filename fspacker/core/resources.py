__all__ = ["resources"]

import logging
import typing

import stdlib_list

from fspacker.conf.settings import settings
from fspacker.core.libraries import LibraryInfo
from fspacker.utils.trackers import perf_tracker

_extern_libs_repo: typing.Dict[str, LibraryInfo] = {}
_builtin_libs_repo: typing.Set[str] = set()


@perf_tracker
def _get_libs_repo() -> typing.Dict[str, LibraryInfo]:
    global _extern_libs_repo

    if not len(_extern_libs_repo):
        lib_files = list(
            _ for _ in settings.libs_dir.rglob("*") if _.suffix in (".whl", ".tar.gz")
        )
        for lib_file in lib_files:
            info = LibraryInfo.from_filepath(lib_file)
            _extern_libs_repo.setdefault(info.meta_data.name.lower(), info)
        logging.info(f"Fetching local library, total: [{len(lib_files)}]")

    return _extern_libs_repo


@perf_tracker
def _get_builtin_repo() -> typing.Set[str]:
    """Analyse and return names of built-in libraries"""
    global _builtin_libs_repo

    if not len(_builtin_libs_repo):
        _builtin_libs_repo = set(stdlib_list.stdlib_list(settings.python_ver_short))
        logging.info(f"Parse built-in libs: total=[{len(_builtin_libs_repo)}]")

    return _builtin_libs_repo


class Resources:
    LIBS_REPO = _get_libs_repo()
    BUILTIN_REPO = _get_builtin_repo()

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Resources()

        return cls._instance


resources = Resources.get_instance()
