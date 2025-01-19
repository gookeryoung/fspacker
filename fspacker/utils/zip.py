import logging
import pathlib
import typing


def get_zip_meta_data(filepath: pathlib.Path) -> typing.Tuple[str, str]:
    if filepath.suffix == ".whl":
        name, version, *_ = filepath.name.split("-")
        name = name.replace("_", "-")
    elif filepath.suffix == ".gz":
        name, version = filepath.name.rsplit("-", 1)
    else:
        logging.error(f"[!!!] Lib file [{filepath.name}] not valid")
        name, version = "", ""

    return name.lower(), version.lower()
