import pathlib

import pkginfo


def parse_libname(filepath: pathlib.Path) -> str:
    """
    Parse lib name from filepath.

    :param filepath: Input file path.
    :return: Lib name parsed.
    """
    meta_data = pkginfo.get_metadata(str(filepath))
    if hasattr(meta_data, "name"):
        return meta_data.name
    else:
        raise ValueError(f"Lib name not found in {filepath.name}")
