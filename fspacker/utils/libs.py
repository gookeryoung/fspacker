import logging
import pathlib
import re
import typing

import pkginfo

from fspacker.conf.settings import settings
from fspacker.core.archive import unpack
from fspacker.core.libraryinfo import LibraryInfo
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
    try:
        meta_data = pkginfo.get_metadata(str(filepath))
        if meta_data is not None and meta_data.name is not None:
            logging.info(
                f"Parsed library name: [{meta_data.name.lower()}] from [{filepath}]"
            )
            return meta_data.name.lower()
        else:
            logging.warning(f"No valid metadata found in [{filepath}]")
            return None
    except Exception as e:
        logging.error(
            f"Error occurred while parsing library name from [{filepath}]: {e}"
        )
        return None


def get_lib_meta_depends(filepath: pathlib.Path) -> typing.Set[str]:
    """Get requires dist of lib file."""
    try:
        meta_data = pkginfo.get_metadata(str(filepath))
        if meta_data is not None and hasattr(meta_data, "requires_dist"):
            dependencies = set(
                re.split(r"[;<>!=()\[~.]", x)[0].strip()
                for x in meta_data.requires_dist
            )
            logging.info(f"Dependencies for library [{filepath.name}]: {dependencies}")
            return dependencies
        else:
            logging.warning(f"No requires found in metadata for [{filepath}]")
            return set()
    except Exception as e:
        logging.error(
            f"Error occurred while getting dependencies for [{filepath}]: {e}"
        )
        return set()


@perf_tracker
def install_lib(
    libname: str,
    target: PackTarget,
    patterns: typing.Optional[typing.Set[str]] = None,
    excludes: typing.Optional[typing.Set[str]] = None,
    extend_depends: bool = False,
) -> bool:
    lib_path = target.packages_dir / libname
    if lib_path.exists():
        logging.info("Lib file already exists, exit.")
        return False

    info = resources.libs_repo.get(libname.lower())
    if info is None or not info.filepath.exists():
        if settings.config.get("mode.offline", None) is True:
            logging.error(f"[!!!] Offline mode, lib [{libname}] not found")
            return False

        filepath = download_wheel(libname)
        if filepath and filepath.exists():
            resources.libs_repo[libname] = LibraryInfo.from_filepath(filepath)
            unpack(filepath, target.packages_dir)
    else:
        filepath = info.filepath
        unpack_wheel(libname, target.packages_dir, patterns, excludes)

    if extend_depends and filepath and filepath.exists():
        target.depends.libs |= get_lib_meta_depends(filepath)

    return True
