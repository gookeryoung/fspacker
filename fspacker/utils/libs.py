import logging
import pathlib
import re
import subprocess
import typing

import pkginfo

from fspacker.conf.settings import settings
from fspacker.core.libraries import LibraryInfo
from fspacker.parsers.target import PackTarget
from fspacker.utils.resources import resources
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


def unpack_zipfile(filepath: pathlib.Path, dest_dir: pathlib.Path):
    logging.info(f"Unpacking zip file [{filepath.name}] -> [{dest_dir}]")
    subprocess.call(
        [
            "python",
            "-m",
            "pip",
            "install",
            str(filepath),
            "-t",
            str(dest_dir),
            "--no-index",
            "--find-links",
            str(filepath.parent),
        ],
    )


@perf_tracker
def install_lib(
    libname: str,
    target: PackTarget,
    patterns: typing.Optional[typing.Set[str]] = None,
    excludes: typing.Optional[typing.Set[str]] = None,
    extend_depends: bool = False,
) -> bool:
    info: LibraryInfo = resources.LIBS_REPO.get(libname.lower())
    if info is None or not info.filepath.exists():
        if settings.CONFIG.get("mode.offline", None) is None:
            logging.error(f"[!!!] Offline mode, lib [{libname}] not found")
            return False

        filepath = download_wheel(libname)
        if filepath and filepath.exists():
            resources.LIBS_REPO[libname] = LibraryInfo.from_filepath(filepath)
    else:
        filepath = info.filepath
        unpack_wheel(libname, target.packages_dir, patterns, excludes)

    if extend_depends and filepath is not None and filepath.exists():
        lib_depends = get_lib_meta_depends(filepath)
        target.depends.libs |= lib_depends

    return True
