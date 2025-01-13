import logging
import pathlib
import re
import typing

import pkginfo

from fspacker.conf.settings import settings
from fspacker.core.archive import unpack
from fspacker.core.libraries import LibraryInfo
from fspacker.core.resources import resources
from fspacker.core.target import PackTarget
from fspacker.utils.trackers import perf_tracker
from fspacker.utils.wheel import unpack_wheel, download_wheel


def get_lib_meta_name(filepath: pathlib.Path) -> typing.Optional[str]:
    """
    Parse lib name from filepath.

    :param filepath: Input file path.
    :return: Lib name parsed.
    """
    meta_data = pkginfo.get_metadata(str(filepath))
    if meta_data is not None and meta_data.name is not None:
        return meta_data.name.lower()
    else:
        return None


def get_lib_meta_depends(filepath: pathlib.Path) -> typing.Set[str]:
    """Get requires dist of lib file"""
    meta_data = pkginfo.get_metadata(str(filepath))
    if meta_data is not None and hasattr(meta_data, "requires_dist"):
        return set(
            list(
                re.split(r"[;<>!=()\[~.]", x)[0].strip()
                for x in meta_data.requires_dist
            )
        )
    else:
        raise ValueError(f"No requires for {filepath}")


@perf_tracker
def install_lib(
    libname: str,
    target: PackTarget,
    patterns: typing.Optional[typing.Set[str]] = None,
    excludes: typing.Optional[typing.Set[str]] = None,
    extend_depends: bool = False,
) -> bool:
    if (target.packages_dir / libname).exists():
        logging.info("Lib file already exists, exit.")
        return

    info: LibraryInfo = resources.LIBS_REPO.get(libname.lower())
    if info is None or not info.filepath.exists():
        if settings.config.get("mode.offline", None) is None:
            logging.error(f"[!!!] Offline mode, lib [{libname}] not found")
            return False

        filepath = download_wheel(libname)
        if filepath and filepath.exists():
            resources.LIBS_REPO[libname] = LibraryInfo.from_filepath(filepath)
            unpack(filepath, target.packages_dir)
    else:
        filepath = info.filepath
        unpack_wheel(libname, target.packages_dir, patterns, excludes)

    if extend_depends and filepath is not None and filepath.exists():
        lib_depends = get_lib_meta_depends(filepath)
        target.depends.libs |= lib_depends

    return True
