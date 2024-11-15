import logging
import pathlib
import subprocess
import typing
import zipfile

from fspacker.config import LIBS_REPO_DIR


def download_install_wheel(libname: str, dst: pathlib.Path):
    """Download a wheel using pip."""
    download_wheel(libname)

    logging.info(f"Install wheel for {libname}")
    subprocess.call(
        [
            "python",
            "-m",
            "pip",
            "install",
            libname,
            "-t",
            str(dst),
            "--no-index",
            "--find-links",
            str(LIBS_REPO_DIR),
        ],
    )


def download_wheel(libname):
    lib_files = list(_ for _ in LIBS_REPO_DIR.rglob(f"{libname}*"))
    if not lib_files:
        logging.warning(f"No wheel for {libname}, start downloading.")
        subprocess.call(
            [
                "python",
                "-m",
                "pip",
                "download",
                libname,
                "-d",
                str(LIBS_REPO_DIR),
            ],
        )
        lib_files = list(_ for _ in LIBS_REPO_DIR.rglob(f"{libname}*"))

    if len(lib_files):
        return lib_files[0]
    else:
        return None


def get_wheel_dependencies(wheel_file: pathlib.Path) -> typing.Set[str]:
    """Get dependencies from a wheel file"""
    with zipfile.ZipFile(wheel_file, "r") as zip_ref:
        metadata_file = next(
            (name for name in zip_ref.namelist() if name.endswith("METADATA")),
            None,
        )
        if not metadata_file:
            raise FileNotFoundError("METADATA file not found in the wheel file")

        with zip_ref.open(metadata_file) as f:
            metadata = f.read().decode("utf-8")

    dependencies = set()
    for line in metadata.splitlines():
        if line.startswith("Requires-Dist:"):
            dependency = line.split(":", 1)[1].strip()
            dependencies.add(dependency)

    return dependencies
