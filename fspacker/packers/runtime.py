import logging
import shutil
import ssl
import time
import urllib.request
from urllib.parse import urlparse

from fspacker.conf.settings import settings
from fspacker.core.target import PackTarget
from fspacker.packers.base import BasePacker
from fspacker.utils.checksum import calc_checksum
from fspacker.utils.url import get_fastest_embed_url


def _safe_read_url_data(url, timeout=10):
    """Open url safely, only allows https schema."""
    parsed_url = urlparse(url)
    allowed_schemes = {"https"}

    try:
        if parsed_url.scheme not in allowed_schemes:
            raise ValueError(f"Unsupported URL scheme: {parsed_url.scheme}")

        # create context with ssl verification
        context = ssl.create_default_context()

        with urllib.request.urlopen(url, timeout=timeout, context=context) as response:
            content = response.read(1024 * 1024 * 100)  # limited to 100MB
            return content
    except ValueError as e:
        logging.error(f"Read url data error, {e}")
        return None


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
        archive_url = f"{fastest_url}{settings.python_ver}/{settings.embed_filename}"
        if not archive_url.startswith("https://"):
            logging.error(
                f"Unsupported archive url: {archive_url}, should starts with `https://`"
            )
            return

        content = _safe_read_url_data(archive_url)
        logging.info(f"Download embed runtime from [{fastest_url}]")
        t0 = time.perf_counter()
        with open(settings.embed_filepath, "wb") as f:
            f.write(content)
        logging.info(
            f"Download finished, total used: [{time.perf_counter() - t0:.2f}]s."
        )

        checksum = calc_checksum(settings.embed_filepath)
        logging.info(f"Write checksum [{checksum}] into config file")
        settings.config["file.embed.checksum"] = checksum
