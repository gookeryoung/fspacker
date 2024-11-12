import dataclasses
import logging
import pathlib
import typing

from fspacker.dirs import get_lib_dir

__all__ = ("fetch_libs_repo",)


@dataclasses.dataclass
class LibraryInfo:
    name: str
    filepath: pathlib.Path

    def __repr__(self):
        return f"[name={self.name}, filepath={self.filepath}]"


_libs_repo: typing.Dict[str, LibraryInfo] = {}


def _setup_library_repo() -> None:
    lib_dir = get_lib_dir()
    lib_files = list(
        _ for _ in lib_dir.rglob("*") if _.suffix in (".whl", ".tar.gz")
    )
    logging.info(f"获取库文件, 总数: {len(lib_files)}")
    for lib_file in lib_files:
        _libs_repo.setdefault(
            lib_file.stem,
            LibraryInfo(name=lib_file.stem, filepath=lib_file),
        )


def fetch_libs_repo() -> typing.Dict[str, LibraryInfo]:
    global _libs_repo

    if not _libs_repo:
        _setup_library_repo()

    return _libs_repo
