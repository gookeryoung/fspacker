import hashlib
import logging
import pathlib
import shutil
import time
from urllib.request import urlopen

from fspacker.config import EMBED_FILE_NAME, EMBED_FILEPATH, PYTHON_VER
from fspacker.packer.base import BasePacker
from fspacker.parser.target import PackTarget
from fspacker.utils.persist import get_json_value, update_json_values
from fspacker.utils.url import get_fastest_embed_url


def _calc_checksum(filepath: pathlib.Path, block_size=4096) -> str:
    """Calculate checksum of filepath, using md5 algorithm.

    Args:
        filepath (pathlib.Path): input filepath.
        block_size (int, optional): read block size, default by 4096.
    """

    hasher = hashlib.md5()
    logging.info(f"Calculate checksum for: [{filepath.name}]")
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(block_size), b""):
            hasher.update(chunk)
    logging.info(f"Checksum is: [{hasher.hexdigest()}]")
    return hasher.hexdigest()


class RuntimePacker(BasePacker):
    def pack(self, target: PackTarget):
        dest = target.runtime_dir
        if (dest / "python.exe").exists():
            logging.info("Runtime folder exists, skip")
            return

        self.fetch_runtime()
        logging.info(
            f"Unpack runtime zip file: [{EMBED_FILEPATH.name}]->[{dest.relative_to(target.root_dir)}]"
        )
        shutil.unpack_archive(EMBED_FILEPATH, dest, "zip")

    @staticmethod
    def fetch_runtime():
        """Fetch runtime zip file"""
        from fspacker.config import EMBED_FILEPATH as EMBED

        if EMBED.exists():
            logging.info(f"Compare file [{EMBED.name}] with local config checksum")
            src_checksum = get_json_value("embed_file_checksum")
            dst_checksum = _calc_checksum(EMBED)
            if src_checksum == dst_checksum:
                logging.info("Checksum matches!")
                return

        fastest_url = get_fastest_embed_url()
        archive_url = f"{fastest_url}{PYTHON_VER}/{EMBED_FILE_NAME}"
        with urlopen(archive_url) as url:
            runtime_files = url.read()

        logging.info(f"Download embed runtime from [{fastest_url}]")
        t0 = time.perf_counter()
        with open(EMBED, "wb") as f:
            f.write(runtime_files)
        logging.info(
            f"Download finished, total used: [{time.perf_counter() - t0:.2f}]s."
        )

        checksum = _calc_checksum(EMBED)
        logging.info(f"Write checksum [{checksum}] into config file")
        update_json_values(dict(embed_file_checksum=checksum))
