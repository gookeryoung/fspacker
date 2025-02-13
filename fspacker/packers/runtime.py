import logging
import shutil
import ssl
import time
import urllib.request
from typing import Optional
from urllib.parse import urlparse

from fspacker.conf.settings import settings
from fspacker.core.target import PackTarget
from fspacker.packers.base import BasePacker
from fspacker.utils.checksum import calc_checksum
from fspacker.utils.url import get_fastest_embed_url


def _safe_read_url_data(url: str, timeout: int = 10) -> Optional[bytes]:
    """Safely read data from a URL with HTTPS schema.

    Args:
        url: The URL to read from.
        timeout: Connection timeout in seconds.

    Returns:
        The content as bytes if successful, None otherwise.
    """
    parsed_url = urlparse(url)
    allowed_schemes = {"https"}

    try:
        if parsed_url.scheme not in allowed_schemes:
            raise ValueError(f"Unsupported URL scheme: {parsed_url.scheme}")

        context = ssl.create_default_context()
        with urllib.request.urlopen(url, timeout=timeout, context=context) as response:
            return response.read(1024 * 1024 * 100)  # limited to 100MB
    except (ValueError, urllib.error.URLError) as e:
        logging.error(f"Failed to read URL data: {e}")
        return None


class RuntimePacker(BasePacker):
    """Handles the packing of runtime dependencies."""

    def pack(self, target: PackTarget) -> None:
        """Pack runtime dependencies into the target directory.

        Args:
            target: The target configuration for packing.
        """
        dest = target.runtime_dir
        if (dest / "python.exe").exists():
            logging.info("Runtime folder exists, skipping")
            return

        if not settings.is_offline_mode:
            self.fetch_runtime()

        logging.info(
            f"Unpacking runtime: [{settings.embed_filepath.name}] -> [{dest.relative_to(target.root_dir)}]"
        )
        shutil.unpack_archive(settings.embed_filepath, dest, "zip")

    @staticmethod
    def fetch_runtime() -> None:
        """Fetch runtime zip file from the fastest available mirror."""
        if settings.embed_filepath.exists():
            logging.info(f"Checking [{settings.embed_filepath.name}] checksum")
            src_checksum = settings.config.get("file.embed.checksum", "")
            dst_checksum = calc_checksum(settings.embed_filepath)
            if src_checksum == dst_checksum:
                logging.info("Checksum matches, using cached runtime")
                return

        fastest_url = get_fastest_embed_url()
        archive_url = f"{fastest_url}{settings.python_ver}/{settings.embed_filename}"

        if not archive_url.startswith("https://"):
            logging.error(f"Invalid archive URL: {archive_url}")
            return

        content = _safe_read_url_data(archive_url)
        if content is None:
            logging.error("Failed to download runtime")
            return

        logging.info(f"Downloading runtime from [{fastest_url}]")
        t0 = time.perf_counter()

        with open(settings.embed_filepath, "wb") as f:
            f.write(content)

        download_time = time.perf_counter() - t0
        logging.info(f"Download completed in [{download_time:.2f}]s")

        checksum = calc_checksum(settings.embed_filepath)
        logging.info(f"Updating checksum [{checksum}]")
        settings.config["file.embed.checksum"] = checksum
