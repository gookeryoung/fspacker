import logging
import shutil
import time
from urllib.request import urlopen

from fspacker.config import EMBED_FILE_NAME, EMBED_FILEPATH, PYTHON_VER
from fspacker.packers.base import BasePacker
from fspacker.parsers.target import PackTarget
from fspacker.utils.checksum import calc_checksum
from fspacker.utils.config import ConfigManager
from fspacker.utils.url import get_fastest_embed_url


class RuntimePacker(BasePacker):
    def __init__(self):
        super().__init__()

    def pack(self, target: PackTarget):
        dest = target.runtime_dir
        if (dest / "python.exe").exists():
            logging.info("Runtime folder exists, skip")
            return

        config = ConfigManager.get_instance()
        if not config["mode.offline"]:
            self.fetch_runtime()

        logging.info(f"Unpack runtime zip file: [{EMBED_FILEPATH.name}]->[{dest.relative_to(target.root_dir)}]")
        shutil.unpack_archive(EMBED_FILEPATH, dest, "zip")

    @staticmethod
    def fetch_runtime():
        """Fetch runtime zip file"""

        config = ConfigManager.get_instance()
        if EMBED_FILEPATH.exists():
            logging.info(f"Compare file [{EMBED_FILEPATH.name}] with local config checksum")
            src_checksum = config["file.embed.checksum"]
            dst_checksum = calc_checksum(EMBED_FILEPATH)
            if src_checksum == dst_checksum:
                logging.info("Checksum matches!")
                return

        fastest_url = get_fastest_embed_url()
        archive_url = f"{fastest_url}{PYTHON_VER}/{EMBED_FILE_NAME}"
        with urlopen(archive_url) as url:
            runtime_files = url.read()

        logging.info(f"Download embed runtime from [{fastest_url}]")
        t0 = time.perf_counter()
        with open(EMBED_FILEPATH, "wb") as f:
            f.write(runtime_files)
        logging.info(f"Download finished, total used: [{time.perf_counter() - t0:.2f}]s.")

        checksum = calc_checksum(EMBED_FILEPATH)
        logging.info(f"Write checksum [{checksum}] into config file")
        config["file.embed.checksum"] = checksum
