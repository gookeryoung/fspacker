import hashlib
import json
import logging
import pathlib
import shutil
import time
import typing
from urllib.request import urlopen

import requests
from fspacker.common import PackTarget
from fspacker.config import EMBED_FILEPATH, EMBED_FILE_NAME, PYTHON_VER
from fspacker.config import EMBED_URL_PREFIX
from fspacker.packer.base import BasePacker


def _calc_checksum(filepath: pathlib.Path, algorithm="md5", block_size=4096) -> str:
    """Calculate checksum of filepath.

    Args:
        filepath (pathlib.Path): input filepath.
        algorithm (str, optional): checksum algorithm, default by "md5".
        block_size (int, optional): read block size, default by 4096.
    """
    if algorithm == "md5":
        hasher = hashlib.md5()
    elif algorithm == "sha1":
        hasher = hashlib.sha1()
    elif algorithm == "sha256":
        hasher = hashlib.sha256()
    else:
        raise ValueError(f"Unsupported algorithm: [{algorithm}]")

    logging.info(f"Calculate checksum for: [{filepath.name}]")
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(block_size), b""):
            hasher.update(chunk)
    logging.info(f"Checksum is: [{hasher.hexdigest()}]")
    return hasher.hexdigest()


def _get_json_value(filepath: pathlib.Path, key: str) -> typing.Any:
    with open(filepath) as f:
        data = json.load(f)
        return data.setdefault(key, None)


def _update_json_values(filepath: pathlib.Path, updates: typing.Dict[str, typing.Any]):
    """Update [key, value] in json file

    Args:
        filepath (pathlib.Path): Input file
        updates (typing.Dict[str, typing.Any]): update values
    """
    if filepath.exists():
        with open(filepath) as fr:
            data = json.load(fr)
    else:
        data = {}

    for key, value in updates.items():
        data[key] = value

    with open(filepath, "w") as fw:
        json.dump(data, fw, indent=4, ensure_ascii=False)


def _check_url_access_time(url: str) -> float:
    """Check access time for url"""
    start = time.perf_counter()
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        time_used = time.perf_counter() - start
        logging.info(f"Access time [{time_used:.2f}]s for [{url}]")
        return time_used
    except requests.exceptions.RequestException:
        logging.info(f"Access time out, url: [{url}]")
        return -1


def _check_fastest_url() -> str:
    """Check fastest url for embed python."""
    min_time, fastest_url = 10.0, ""
    for name, embed_url in EMBED_URL_PREFIX.items():
        time_used = _check_url_access_time(embed_url)
        if time_used > 0:
            if time_used < min_time:
                fastest_url = embed_url
                min_time = time_used

    logging.info(f"Found fastest url: [{fastest_url}]")
    return fastest_url


class RuntimePacker(BasePacker):
    def pack(self, target: PackTarget):
        dest = target.runtime_dir
        if not dest.exists():
            logging.info(f"Create runtime folder: [{dest}]")
            dest.mkdir(parents=True)

        if not EMBED_FILEPATH.exists():
            self.fetch_runtime()

        logging.info(f"Unpack runtime zip file: [{EMBED_FILEPATH.name}]->[{dest}]")
        try:
            shutil.unpack_archive(EMBED_FILEPATH, dest, "zip")
            return True
        except ValueError as e:
            logging.error(f"Unpack failed, message: {e}")
            return False

    @staticmethod
    def fetch_runtime():
        """Fetch runtime zip file"""
        from fspacker.config import EMBED_FILEPATH as EMBED, EMBED_REPO_DIR
        from fspacker.config import CONFIG_FILEPATH as CFG

        if not EMBED_REPO_DIR.exists():
            EMBED_REPO_DIR.mkdir(parents=True)

        if EMBED.exists():
            logging.info(f"Compare file [{EMBED.name}] with local config [{CFG.name}] checksum")
            src_checksum = _get_json_value(CFG, "embed_file_checksum")
            dst_checksum = _calc_checksum(EMBED)
            if src_checksum == dst_checksum:
                logging.info("Checksum matches!")
                return

        logging.info("Fetch fastest embed python url")
        fastest_url = _check_fastest_url()
        archive_url = f"{fastest_url}{PYTHON_VER}/{EMBED_FILE_NAME}"
        with urlopen(archive_url) as url:
            runtime_files = url.read()

        logging.info(f"Download embed runtime from [{fastest_url}]")
        t0 = time.perf_counter()
        with open(EMBED, "wb") as f:
            f.write(runtime_files)
        logging.info(f"Download finished, total used: [{time.perf_counter() - t0:.2f}]s.")

        checksum = _calc_checksum(EMBED)
        logging.info(f"Write checksum [{checksum}] into config file [{CFG}]")
        _update_json_values(CFG, dict(embed_file_checksum=checksum))
