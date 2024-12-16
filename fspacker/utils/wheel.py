import logging
import pathlib
import re
import subprocess
import typing
import zipfile
from urllib.parse import urlparse

from fspacker.config import LIBS_REPO_DIR
from fspacker.utils.repo import get_libs_repo, map_libname
from fspacker.utils.url import get_fastest_pip_url


def unpack_wheel(
    libname: str,
    dest_dir: pathlib.Path,
    patterns: typing.Set[str],
    excludes: typing.Set[str],
) -> None:
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
        logging.info(
            f"Unpacking by pattern [{info.filepath.name}]->[{dest_dir.name}]"
        )
        with zipfile.ZipFile(info.filepath, "r") as zip_ref:
            for file in zip_ref.namelist():
                if any(e.match(file) for e in compiled_excludes):
                    continue

                if len(patterns) and any(
                    p.match(file) for p in compiled_patterns
                ):
                    zip_ref.extract(file, dest_dir)
                    continue

                zip_ref.extract(file, dest_dir)


def download_wheel(libname) -> pathlib.Path:
    real_libname = _normalize_libname(map_libname(libname))

    lib_files = list(_ for _ in LIBS_REPO_DIR.rglob(f"{real_libname}*"))
    if not lib_files:
        logging.warning(f"No wheel for {real_libname}, start downloading.")
        pip_url = get_fastest_pip_url()
        net_loc = urlparse(pip_url).netloc
        subprocess.call(
            [
                "python",
                "-m",
                "pip",
                "download",
                real_libname,
                "-d",
                str(LIBS_REPO_DIR),
                "--trusted-host",
                net_loc,
                "-i",
                pip_url,
            ],
        )
        lib_files = list(
            _
            for pattern in (libname, real_libname)
            for _ in LIBS_REPO_DIR.rglob(f"{pattern}*")
        )

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
    elif "~=" in lib_str:
        return lib_str.split("~=")[0]
    elif "[" in lib_str and "]" in lib_str:
        return lib_str.split("[")[0]
    else:
        return lib_str
