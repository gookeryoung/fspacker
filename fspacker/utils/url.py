import logging
import time
import typing

import requests

from fspacker.config import EMBED_URL_PREFIX, PIP_URL_PREFIX
from fspacker.utils.config import ConfigManager
from fspacker.utils.performance import perf_tracker

__all__ = [
    "get_fastest_embed_url",
    "get_fastest_pip_url",
]


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


def _get_fastest_url(urls: typing.Dict[str, str]) -> str:
    """Check fastest url for embed python."""
    min_time, fastest_url = 10.0, ""
    for name, embed_url in urls.items():
        time_used = _check_url_access_time(embed_url)
        if time_used > 0:
            if time_used < min_time:
                fastest_url = embed_url
                min_time = time_used

    logging.info(f"Found fastest url: [{fastest_url}]")
    return fastest_url


@perf_tracker
def get_fastest_pip_url() -> str:
    config = ConfigManager()
    if fastest_url := config["fastest_pip_url"]:
        return fastest_url
    else:
        fastest_url = _get_fastest_url(PIP_URL_PREFIX)
        config["fastest_pip_url"] = fastest_url
        return fastest_url


@perf_tracker
def get_fastest_embed_url() -> str:
    config = ConfigManager()
    if fastest_url := config["fastest_embed_url"]:
        return fastest_url
    else:
        fastest_url = _get_fastest_url(EMBED_URL_PREFIX)
        config["fastest_embed_url"] = fastest_url
        return fastest_url
