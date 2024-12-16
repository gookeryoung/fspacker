import pathlib
import typing

import pkginfo


def get_lib_name(filepath: pathlib.Path) -> str:
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


def get_lib_depends(filepath: pathlib.Path) -> typing.Set[str]:
    """Get requires dist of lib file"""
    meta_data = pkginfo.get_metadata(str(filepath))
    if hasattr(meta_data, "requires_dist"):
        return set(list(x.split(" ")[0] for x in meta_data.requires_dist))
    else:
        raise ValueError(f"No requires for {filepath}")
