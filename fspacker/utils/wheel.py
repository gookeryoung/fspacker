import logging
import pathlib
import re
import shutil
import subprocess
import typing
import zipfile
from urllib.parse import urlparse

from fspacker.config import LIBS_REPO_DIR
from fspacker.utils.repo import get_libs_repo
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
            f"Unpacking by pattern [{info.meta_data.name}]->[{dest_dir.name}]"
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


def download_wheel(libname: str) -> pathlib.Path:
    """Download wheel file for lib name, if not found in lib repo."""

    match_name = "*".join(re.split(r"[-_]", libname))
    lib_files = list(_ for _ in LIBS_REPO_DIR.rglob(f"{match_name}*"))
    if not lib_files:
        logging.warning(f"No wheel for {libname}, start downloading.")
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
        lib_files = list(_ for _ in LIBS_REPO_DIR.rglob(f"{match_name}*"))

    assert len(lib_files)
    return lib_files[0]


def remove_wheel(libname: str) -> None:
    """Remove wheel file in repo."""

    info = get_libs_repo().get(libname)
    if info is not None:
        if info.filepath.exists():
            info.filepath.unlink()
            logging.info(f"Remove wheel file [{info.filepath.name}]")
