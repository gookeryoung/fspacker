import logging
import time
import typing

import requests

from fspacker.config import PIP_URL_PREFIX, EMBED_URL_PREFIX
from fspacker.utils.persist import get_json_value, update_json_values

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


def get_fastest_pip_url() -> str:
    if fastest_url := get_json_value("fastest_pip_url"):
        return fastest_url
    else:
        fastest_url = _get_fastest_url(PIP_URL_PREFIX)
        update_json_values(dict(fastest_pip_url=fastest_url))
        return fastest_url


def get_fastest_embed_url() -> str:
    if fastest_url := get_json_value("fastest_embed_url"):
        return fastest_url
    else:
        fastest_url = _get_fastest_url(EMBED_URL_PREFIX)
        update_json_values(dict(fastest_embed_url=fastest_url))
        return fastest_url
