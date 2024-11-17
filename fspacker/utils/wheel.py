import functools
import logging
import pathlib
import re
import subprocess
import typing
import zipfile

from importlib_metadata import PackageNotFoundError, requires

from fspacker.config import LIBS_REPO_DIR
from fspacker.utils.repo import get_libs_repo


def unpack_wheel(libname: str, dest_dir: pathlib.Path, patterns: typing.Set[str]) -> None:
    info = get_libs_repo().get(libname)

    if info is not None:
        if not len(patterns):
            patterns = {
                f"{libname}.*.py[cdo]?",
                f"{libname}/.*",
                f"{libname}-data/.*",
            }

        compiled_patterns = [re.compile(f".*{pattern}") for pattern in patterns]
        logging.info(f"Unpacking by pattern [{info.filepath.name}]->[{dest_dir.name}]")
        with zipfile.ZipFile(info.filepath, "r") as zip_ref:
            for file in zip_ref.namelist():
                if any(pattern.match(file) for pattern in compiled_patterns):
                    zip_ref.extract(file, dest_dir)


def download_wheel(libname) -> pathlib.Path:
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

    raise FileNotFoundError(f"No wheel file for {libname}")


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
            dependencies.add(dependency.split(" ")[0])

    return dependencies


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
    if depth >= 3:
        return set()

    try:
        requires_ = requires(package_name)
        names = set()
        if requires_:
            for req in requires_:
                names.add(_normalize_libname(req))

        for name in names:
            names = names.union(get_dependencies(name, depth + 1))

        return names
    except PackageNotFoundError as e:
        logging.info(f"Error processing package {package_name}: {e}")
        return set()
