import logging
import shutil
import time

from fspacker.common import BuildTarget
from fspacker.dirs import (
    get_embed_filepath,
    get_runtime_dir,
)
from fspacker.packer.base import BasePacker


class RuntimePacker(BasePacker):
    def pack(self, target: BuildTarget):
        embed = get_embed_filepath()
        dest = get_runtime_dir(target.src.parent)
        if not dest.exists():
            logging.info(f"创建项目运行时文件夹: [{dest}]")
            dest.mkdir(parents=True)

        logging.info(f"解压运行时文件[{embed.name}]->[{dest}]")
        t0 = time.perf_counter()
        try:
            shutil.unpack_archive(embed, dest, "zip")
            logging.info(f"解压完成, 用时: {time.perf_counter() - t0:.2f}s.")
            return True
        except ValueError as e:
            logging.error(f"解压失败, 信息: {e}")
            return False
