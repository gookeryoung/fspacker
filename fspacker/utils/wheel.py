import functools
import logging
import pathlib
import re
import subprocess
import typing
import zipfile
from importlib.metadata import PackageNotFoundError, requires
from urllib.parse import urlparse

from fspacker.config import LIBS_REPO_DIR
from fspacker.utils.repo import get_libs_repo
from fspacker.utils.url import get_fastest_pip_url


def unpack_wheel(libname: str, dest_dir: pathlib.Path, patterns: typing.Set[str], excludes: typing.Set[str]) -> None:
    info = get_libs_repo().get(libname)

    if info is None or not info.filepath.exists():
        download_wheel(libname)

    if info is not None:
        if not len(excludes):
            excludes = {
                "dist-info/",
            }

        compiled_patterns = [re.compile(f".*{p}") for p in patterns]
        compiled_excludes = [re.compile(f".*{e}") for e in excludes]
        logging.info(f"Unpacking by pattern [{info.filepath.name}]->[{dest_dir.name}]")
        with zipfile.ZipFile(info.filepath, "r") as zip_ref:
            for file in zip_ref.namelist():
                if any(e.match(file) for e in compiled_excludes):
                    continue

                if len(patterns) and any(p.match(file) for p in compiled_patterns):
                    zip_ref.extract(file, dest_dir)
                    continue

                zip_ref.extract(file, dest_dir)


def download_wheel(libname) -> pathlib.Path:
    lib_files = list(_ for _ in LIBS_REPO_DIR.rglob(f"{libname}*"))
    if not lib_files:
        logging.warning(f"No wheel for {libname}, start downloading.")

        logging.info("Fetch fastest pip url")
        pip_url = get_fastest_pip_url()
        net_loc = urlparse(pip_url).netloc
        subprocess.call(
            [
                "python",
                "-m",
                "pip",
                "download",
                libname,
                "-d",
                str(LIBS_REPO_DIR),
                "--trusted-host",
                net_loc,
                "-i",
                pip_url,
            ],
        )
        lib_files = list(_ for _ in LIBS_REPO_DIR.rglob(f"{libname}*"))

    if len(lib_files):
        return lib_files[0]
    else:
        raise FileNotFoundError(f"No wheel for {libname}")


def _normalize_libname(lib_str: str) -> str:
    lib_str = lib_str.split(";")[0].split(" ")[0]

    if "<" in lib_str:
        return lib_str.split("<")[0]
    elif ">" in lib_str:
        return lib_str.split(">")[0]
    elif "!=" in lib_str:
        return lib_str.split("!=")[0]
    elif "==" in lib_str:
        return lib_str.split("==")[0]
    else:
        return lib_str


@functools.lru_cache(maxsize=128)
def get_dependencies(package_name: str, depth: int) -> typing.Set[str]:
    if depth >= 2:
        return set()

    try:
        requires_ = requires(package_name)
        names = set()
        if requires_:
            for req in requires_:
                names.add(_normalize_libname(req).lower())

        for name in names:
            names = names.union(get_dependencies(name, depth + 1))

        return names
    except PackageNotFoundError:
        logging.warning(f"Could not find package meta data for [{package_name}]")
        return set()
