import dataclasses
import logging
import pathlib
import typing

from pkginfo import Distribution

from fspacker.conf.settings import settings


@dataclasses.dataclass
class LibraryInfo:
    meta_data: Distribution
    filepath: pathlib.Path

    def __repr__(self):
        return f"{self.meta_data.name}-{self.meta_data.version}"

    @staticmethod
    def from_filepath(filepath: pathlib.Path):
        name, version = get_zip_meta_data(filepath)
        lib_info = LibraryInfo(filepath=filepath, meta_data=Distribution())
        lib_info.meta_data.name = name
        lib_info.meta_data.version = version
        return lib_info


def get_zip_meta_data(filepath: pathlib.Path) -> typing.Tuple[str, str]:
    if filepath.suffix == ".whl":
        name, version, *others = filepath.name.split("-")
        name = name.replace("_", "-")
    elif filepath.suffix == ".gz":
        name, version = filepath.name.rsplit("-", 1)
    else:
        logging.error(f"[!!!] Lib file [{filepath.name}] not valid")
        name, version = "", ""

    return name.lower(), version.lower()


def get_libname(libname: str) -> str:
    libname = _map_libname(libname).lower()
    if "_" in libname:
        return libname.replace("_", "-")
    return libname


def _map_libname(libname: str) -> str:
    if libname in settings.libname_mapper:
        return settings.libname_mapper[libname]

    return libname
