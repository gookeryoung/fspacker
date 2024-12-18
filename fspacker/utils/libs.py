import logging
import pathlib
import re
import subprocess
import typing

import pkginfo


def get_zip_meta_data(filepath: pathlib.Path) -> typing.Tuple[str, str]:
    if filepath.suffix == ".whl":
        name, version, *others = filepath.name.split("-")
    elif filepath.suffix == ".gz":
        name, version = filepath.name.rsplit("-", 1)
    else:
        logging.error(f"[!!!] Lib file [{filepath.name}] not valid")
        name, version = None, None

    return name, version


def get_lib_meta_name(filepath: pathlib.Path) -> str:
    """
    Parse lib name from filepath.

    :param filepath: Input file path.
    :return: Lib name parsed.
    """
    meta_data = pkginfo.get_metadata(str(filepath))
    if hasattr(meta_data, "name"):
        return meta_data.name
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
