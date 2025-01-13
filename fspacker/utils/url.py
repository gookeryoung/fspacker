import logging
import time
import typing

import requests

from fspacker.conf.settings import settings
from fspacker.utils.trackers import perf_tracker

__all__ = [
    "get_fastest_embed_url",
    "get_fastest_pip_url",
]

# python mirrors
EMBED_URL_PREFIX: typing.Dict[str, str] = dict(
    official="https://www.python.org/ftp/python/",
    huawei="https://mirrors.huaweicloud.com/python/",
)

# pip mirrors
PIP_URL_PREFIX: typing.Dict[str, str] = dict(
    aliyun="https://mirrors.aliyun.com/pypi/simple/",
    tsinghua="https://pypi.tuna.tsinghua.edu.cn/simple/",
    ustc="https://pypi.mirrors.ustc.edu.cn/simple/",
    huawei="https://mirrors.huaweicloud.com/repository/pypi/simple/",
)


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
    if fastest_url := settings.config.get("url.pip"):
        return fastest_url
    else:
        fastest_url = _get_fastest_url(PIP_URL_PREFIX)
        settings.config["url.pip"] = fastest_url
        return fastest_url


@perf_tracker
def get_fastest_embed_url() -> str:
    if fastest_url := settings.config.get("url.embed", ""):
        return fastest_url
    else:
        fastest_url = _get_fastest_url(EMBED_URL_PREFIX)
        settings.config["url.embed"] = fastest_url
        return fastest_url
