import logging
import shutil
import time
from urllib.request import urlopen

from fspacker.conf.settings import settings
from fspacker.packers.base import BasePacker
from fspacker.parsers.target import PackTarget
from fspacker.utils.checksum import calc_checksum
from fspacker.utils.url import get_fastest_embed_url


class RuntimePacker(BasePacker):
    def __init__(self):
        super().__init__()

    def pack(self, target: PackTarget):
        dest = target.runtime_dir
        if (dest / "python.exe").exists():
            logging.info("Runtime folder exists, skip")
            return

        if not settings.CONFIG["mode.offline"]:
            self.fetch_runtime()

        logging.info(
            f"Unpack runtime zip file: [{settings.EMBED_FILE_PATH.name}]->[{dest.relative_to(target.root_dir)}]"
        )
        shutil.unpack_archive(settings.EMBED_FILE_PATH, dest, "zip")

    @staticmethod
    def fetch_runtime():
        """Fetch runtime zip file"""

        if settings.EMBED_FILE_PATH.exists():
            logging.info(
                f"Compare file [{settings.EMBED_FILE_PATH.name}] with local config checksum"
            )
            src_checksum = settings.CONFIG.get("file.embed.checksum", "")
            dst_checksum = calc_checksum(settings.EMBED_FILE_PATH)
            if src_checksum == dst_checksum:
                logging.info("Checksum matches!")
                return

        fastest_url = get_fastest_embed_url()
        archive_url = f"{fastest_url}{settings.PYTHON_VER}/{settings.EMBED_FILE_NAME}"
        with urlopen(archive_url) as url:
            runtime_files = url.read()

        logging.info(f"Download embed runtime from [{fastest_url}]")
        t0 = time.perf_counter()
        with open(settings.EMBED_FILE_PATH, "wb") as f:
            f.write(runtime_files)
        logging.info(
            f"Download finished, total used: [{time.perf_counter() - t0:.2f}]s."
        )

        checksum = calc_checksum(settings.EMBED_FILE_PATH)
        logging.info(f"Write checksum [{checksum}] into config file")
        settings.CONFIG["file.embed.checksum"] = checksum
