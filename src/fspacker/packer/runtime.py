import hashlib
import json
import logging
import pathlib
import shutil
import time
import typing
from urllib.request import urlopen

import requests

from fspacker.common import BuildTarget
from fspacker.config import EMBED_FILEPATH, EMBED_FILE_NAME, PYTHON_VER
from fspacker.config import EMBED_URL_PREFIX
from fspacker.packer.base import BasePacker


def _calc_checksum(
    filepath: pathlib.Path, algorithm="md5", block_size=4096
) -> str:
    """计算文件校验和.

    Args:
        filepath (pathlib.Path): 输入文件路径.
        algorithm (str, optional): 校验算法, 默认为 "md5".
        block_size (int, optional): 读取块长度, 默认为 4096.
    """
    if algorithm == "md5":
        hasher = hashlib.md5()
    elif algorithm == "sha1":
        hasher = hashlib.sha1()
    elif algorithm == "sha256":
        hasher = hashlib.sha256()
    else:
        raise ValueError(f"不支持的校验和算法: [{algorithm}]")

    logging.info(f"计算文件[{filepath}]校验和")
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(block_size), b""):
            hasher.update(chunk)
    logging.info(f"计算值[{hasher.hexdigest()}]")
    return hasher.hexdigest()


def _get_json_value(filepath: pathlib.Path, key: str) -> typing.Any:
    with open(filepath) as f:
        data = json.load(f)
        return data.setdefault(key, None)


def _update_json_values(
    filepath: pathlib.Path, updates: typing.Dict[str, typing.Any]
):
    """Update [key, value] in json file

    Args:
        filepath (pathlib.Path): Input file
        updates (typing.Dict[str, typing.Any]): update values
    """
    if filepath.exists():
        with open(filepath) as fr:
            data = json.load(fr)
    else:
        data = {}

    for key, value in updates.items():
        data[key] = value

    with open(filepath, "w") as fw:
        json.dump(data, fw, indent=4, ensure_ascii=False)


def _check_url_access_time(url: str) -> float:
    """检查 url 访问是否超时"""
    start = time.perf_counter()
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        time_used = time.perf_counter() - start
        logging.info(f"{url} 访问用时: {time_used:.2f}s")
        return time_used
    except requests.exceptions.RequestException:
        logging.info(f"{url} 访问超时")
        return -1


def _check_embed_urls() -> str:
    """检查可用镜像"""
    min_time, fastest_url = 10.0, ""
    for name, embed_url in EMBED_URL_PREFIX.items():
        time_used = _check_url_access_time(embed_url)
        if time_used > 0:
            if time_used < min_time:
                fastest_url = embed_url
                min_time = time_used

    logging.info(f"找到最快镜像地址: {fastest_url}")
    return fastest_url


class RuntimePacker(BasePacker):
    def pack(self, target: BuildTarget):
        dest = target.runtime_dir
        if not dest.exists():
            logging.info(f"创建项目运行时文件夹: [{dest}]")
            dest.mkdir(parents=True)

        if not EMBED_FILEPATH.exists():
            self.fetch_runtime()

        logging.info(f"解压运行时文件[{EMBED_FILEPATH.name}]->[{dest}]")
        t0 = time.perf_counter()
        try:
            shutil.unpack_archive(EMBED_FILEPATH, dest, "zip")
            logging.info(f"解压完成, 用时: {time.perf_counter() - t0:.2f}s.")
            return True
        except ValueError as e:
            logging.error(f"解压失败, 信息: {e}")
            return False

    def fetch_runtime(self):
        """获取python运行时"""
        from fspacker.config import EMBED_FILEPATH as EMBED
        from fspacker.config import CONFIG_FILEPATH as CFG

        if EMBED.exists():
            logging.info(f"比较[{EMBED.name}]文件和配置文件[{CFG.name}]校验和")
            src_checksum = _get_json_value(CFG, "embed_file_checksum")
            dst_checksum = _calc_checksum(EMBED)
            if src_checksum == dst_checksum:
                logging.info("校验和相同, 运行时文件检查成功!")
                return

        logging.info("获取 embed python 最佳下载地址")
        fastest_url = _check_embed_urls()
        logging.info(f"已获取地址: [{fastest_url}]")
        archive_url = f"{fastest_url}{PYTHON_VER}/{EMBED_FILE_NAME}"
        logging.info(f"获取压缩包地址: {archive_url}")
        with urlopen(archive_url) as url:
            runtime_files = url.read()

        logging.info(f"从地址[{fastest_url}]下载运行时")
        t0 = time.perf_counter()
        with open(EMBED, "wb") as f:
            f.write(runtime_files)
        logging.info(f"下载完成, 用时: {time.perf_counter() - t0:.2f}s.")

        checksum = _calc_checksum(EMBED)
        logging.info(f"写入校验和[{checksum}]到配置文件{CFG}")
        _update_json_values(CFG, dict(embed_file_checksum=checksum))