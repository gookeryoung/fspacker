import dataclasses
import logging
import pathlib
import typing

import stdlib_list

from fspacker.config import PYTHON_VER_SHORT, LIBS_REPO_DIR

__all__ = (
    "LibraryInfo",
    "fetch_libs_repo",
    "get_libs_std",
)


@dataclasses.dataclass
class LibraryInfo:
    package_name: str
    version: str
    build_tag: str
    abi_tag: str
    platform_tag: str
    filepath: pathlib.Path

    def __repr__(self):
        return self.package_name


_libs_std: typing.List[str] = []
_libs_repo: typing.Dict[str, LibraryInfo] = {}


def _setup_library_repo() -> None:
    lib_files = list(
        _ for _ in LIBS_REPO_DIR.rglob("*") if _.suffix in (".whl", ".tar.gz")
    )
    logging.info(f"获取库文件, 总数: {len(lib_files)}")
    for lib_file in lib_files:
        try:
            package_name, *version, build_tag, abi_tag, platform_tag = (
                lib_file.stem.split("-")
            )
            _libs_repo.setdefault(
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


def fetch_libs_repo() -> typing.Dict[str, LibraryInfo]:
    global _libs_repo

    if not _libs_repo:
        _setup_library_repo()

    return _libs_repo


def get_libs_std() -> typing.List[str]:
    global _libs_std

    if not len(_libs_std):
        _libs_std = stdlib_list.stdlib_list(PYTHON_VER_SHORT)
        logging.info(
            f"获取内置库信息, python {PYTHON_VER_SHORT}\
                共包含[{len(_libs_std)}]个内置库"
        )

    return _libs_std
