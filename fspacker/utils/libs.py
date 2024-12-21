import logging
import pathlib
import re
import subprocess
import typing

import pkginfo

from fspacker.common import LibraryInfo
from fspacker.parser.target import PackTarget
from fspacker.utils.performance import perf_tracker
from fspacker.utils.repo import get_libs_repo, update_libs_repo
from fspacker.utils.wheel import unpack_wheel, download_wheel


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


def get_lib_meta_name(filepath: pathlib.Path) -> str:
    """
    Parse lib name from filepath.

    :param filepath: Input file path.
    :return: Lib name parsed.
    """
    meta_data = pkginfo.get_metadata(str(filepath))
    if hasattr(meta_data, "name"):
        return meta_data.name.lower()
    else:
        raise ValueError(f"Lib name not found in {filepath}")


def get_lib_meta_depends(filepath: pathlib.Path) -> typing.Set[str]:
    """Get requires dist of lib file"""
    meta_data = pkginfo.get_metadata(str(filepath))
    if hasattr(meta_data, "requires_dist"):
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
    patterns: typing.Set[str] = None,
    excludes: typing.Set[str] = None,
    extend_depends: bool = False,
) -> bool:
    info: LibraryInfo = get_libs_repo().get(libname.lower())
    if info is None or not info.filepath.exists():
        filepath = download_wheel(libname)
        if filepath and filepath.exists():
            update_libs_repo(libname, filepath)
    else:
        filepath = info.filepath
        unpack_wheel(libname, target.packages_dir, patterns, excludes)

    if extend_depends and filepath is not None and filepath.exists():
        lib_depends = get_lib_meta_depends(filepath)
        target.depends.libs |= lib_depends
