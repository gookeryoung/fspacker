import fnmatch
import logging
import pathlib
import re
import subprocess
import typing
import zipfile
from urllib.parse import urlparse

from fspacker.core.analyzers import LibraryAnalyzer
from fspacker.core.resources import resources
from fspacker.settings import settings
from fspacker.utils.trackers import perf_tracker
from fspacker.utils.url import get_fastest_pip_url


@perf_tracker
def unpack_wheel(
    libname: str,
    dest_dir: pathlib.Path,
    patterns: typing.Optional[typing.Set[str]] = None,
    excludes: typing.Optional[typing.Set[str]] = None,
) -> None:
    """Unpack wheel file into destination directory."""

    excludes = set() if excludes is None else excludes
    patterns = set() if patterns is None else patterns

    if (dest_dir / libname).exists():
        logging.info(f"Lib [{libname}] already unpacked, skip")
        return

    info = resources.libs_repo.get(libname)
    if info is not None:
        logging.info(f"Unpacking by pattern [{info.meta_data.name}]->[{dest_dir.name}]")

        # No rules, fast unpacking
        # if not len(excludes) and not len(patterns):
        #     shutil.unpack_archive(info.filepath, dest_dir, "zip")
        #     return

        excludes = set(excludes) | {"*dist-info/*"}
        with zipfile.ZipFile(info.filepath, "r") as zip_ref:
            for file in zip_ref.namelist():
                if any(fnmatch.fnmatch(file, exclude) for exclude in excludes):
                    continue

                if len(patterns):
                    if any(fnmatch.fnmatch(file, pattern) for pattern in patterns):
                        zip_ref.extract(file, dest_dir)
                        continue
                    else:
                        continue

                zip_ref.extract(file, dest_dir)
    else:
        logging.error(f"[!!!] Lib {libname} wheel not found.")


@perf_tracker
def download_wheel(libname: str) -> typing.Optional[pathlib.Path]:
    """Download wheel file for lib name, if not found in lib repo."""
    libname = LibraryAnalyzer(libname).metadata.name
    match_name = "*".join(re.split(r"[-_]", libname))
    lib_files = list(_ for _ in settings.libs_dir.rglob(f"{match_name}*"))

    if not lib_files:
        logging.warning(f"No wheel for [{libname}], start downloading.")
        pip_url = get_fastest_pip_url()
        net_loc = urlparse(pip_url).netloc

        try:
            subprocess.check_call(
                [
                    "python",
                    "-m",
                    "pip",
                    "download",
                    libname,
                    "-d",
                    str(settings.libs_dir),
                    "--trusted-host",
                    net_loc,
                    "-i",
                    pip_url,
                ],
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to download wheel [{libname}]: {e}")
            return None

        lib_files = list(_ for _ in settings.libs_dir.rglob(f"{match_name}*"))

    if not len(lib_files):
        logging.error(f"[!!!] Download wheel [{libname}] error, {match_name=}")
        return None

    logging.info(f"Successfully downloaded wheel [{libname}] to [{lib_files[0]}]")
    return lib_files[0]
