import logging

from fspacker.conf.settings import settings
from fspacker.core.resources import resources


def get_libname(libname: str) -> str:
    libname = _map_libname(libname).lower()
    if "_" in libname:
        return libname.replace("_", "-")
    return libname


def _map_libname(libname: str) -> str:
    if libname in settings.libname_mapper:
        return settings.libname_mapper[libname]

    return libname


def get_lib_meta_name(libname: str) -> str:
    """Get the metadata name of the library.

    :param libname: The name of the library.
    :return: The metadata name of the library.
    """
    try:
        info = resources.libs_repo.get(libname)
        if info is None:
            logging.error(f"Library [{libname}] not found in repository.")
            return ""

        meta_name = info.meta_data.name
        logging.info(f"Metadata name for library [{libname}] is [{meta_name}].")
        return meta_name

    except Exception as e:
        logging.error(
            f"Error occurred while getting metadata name for library [{libname}]: {e}"
        )
        return ""
