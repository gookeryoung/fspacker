from fspacker.conf.settings import settings


def _map_libname(libname: str) -> str:
    if libname in settings.libname_mapper:
        return settings.libname_mapper[libname]

    return libname
