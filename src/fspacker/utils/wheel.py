import logging
import pathlib
import subprocess
import typing
import zipfile
from subprocess import CalledProcessError

from fspacker.config import LIBS_REPO_DIR


def download_wheel(libname: str) -> typing.Set[typing.Tuple[str, pathlib.Path]]:
    """Download a wheel using pip."""
    wheel_tree = set()

    try:
        subprocess.call(
            [
                "python",
                "-m",
                "pip",
                "download",
                libname,
                "--no-deps",
                "-d",
                str(LIBS_REPO_DIR),
            ],
        )
        lib_file = list(_ for _ in LIBS_REPO_DIR.rglob(f"{libname}*"))[0]
        logging.info(f"Successfully download {libname}")
        wheel_tree.add((libname, lib_file))

        dependencies = (_.split(" ")[0] for _ in get_wheel_dependencies(lib_file))
        logging.info(f"Parsing dependencies: {dependencies}")
        for dep in dependencies:
            wheel_tree.union(download_wheel(dep))

        return wheel_tree
    except CalledProcessError as e:
        logging.error(f"Failed to download {libname}: {e}")


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
