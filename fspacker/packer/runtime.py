import logging
import shutil
import time
from urllib.request import urlopen

from fspacker.config import EMBED_FILE_NAME, EMBED_FILEPATH, PYTHON_VER
from fspacker.packer.base import BasePacker
from fspacker.parser.target import PackTarget
from fspacker.utils.checksum import calc_checksum
from fspacker.utils.config import get_config_manager
from fspacker.utils.url import get_fastest_embed_url


class RuntimePacker(BasePacker):
    def __init__(self):
        super().__init__()

        self._config = get_config_manager()

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

    def fetch_runtime(self):
        """Fetch runtime zip file"""
        from fspacker.config import EMBED_FILEPATH as EMBED

        if EMBED.exists():
            logging.info(
                f"Compare file [{EMBED.name}] with local config checksum"
            )
            src_checksum = self._config["embed_file_checksum"]
            dst_checksum = calc_checksum(EMBED)
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

        checksum = calc_checksum(EMBED)
        logging.info(f"Write checksum [{checksum}] into config file")
        self._config["embed_file_checksum"] = checksum
