import logging
import shutil
import time
from urllib.request import urlopen

from fspacker.conf.settings import settings
from fspacker.core.target import PackTarget
from fspacker.packers.base import BasePacker
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

        if not settings.config["mode.offline"]:
            self.fetch_runtime()

        logging.info(
            f"Unpack runtime zip file: [{settings.embed_filepath.name}]->[{dest.relative_to(target.root_dir)}]"
        )
        shutil.unpack_archive(settings.embed_filepath, dest, "zip")

    @staticmethod
    def fetch_runtime():
        """Fetch runtime zip file"""

        if settings.embed_filepath.exists():
            logging.info(
                f"Compare file [{settings.embed_filepath.name}] with local config checksum"
            )
            src_checksum = settings.config.get("file.embed.checksum", "")
            dst_checksum = calc_checksum(settings.embed_filepath)
            if src_checksum == dst_checksum:
                logging.info("Checksum matches!")
                return

        fastest_url = get_fastest_embed_url()
        archive_url = f"{fastest_url}{settings.python_ver}/{settings.embed_file_name}"
        with urlopen(archive_url) as url:
            runtime_files = url.read()

        logging.info(f"Download embed runtime from [{fastest_url}]")
        t0 = time.perf_counter()
        with open(settings.embed_filepath, "wb") as f:
            f.write(runtime_files)
        logging.info(
            f"Download finished, total used: [{time.perf_counter() - t0:.2f}]s."
        )

        checksum = calc_checksum(settings.embed_filepath)
        logging.info(f"Write checksum [{checksum}] into config file")
        settings.config["file.embed.checksum"] = checksum
