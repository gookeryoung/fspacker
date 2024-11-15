import logging
import pathlib

from fspacker.config import IGNORE_SYMBOLS
from fspacker.parser.base import BaseParser


class FolderParser(BaseParser):
    """文件夹分析"""

    def parse(self, entry: pathlib.Path):
        if entry.stem.lower() in IGNORE_SYMBOLS:
            logging.info(f"跳过文件夹: [{entry.stem}]")
            return

        for k, v in self.config.targets.items():
            if entry.stem in v.code:
                v.deps.add(entry.stem)
                logging.info(f"更新打包目标: {v}")

            if entry.stem in v.ast:
                v.deps.add(entry.stem)
                v.ast.remove(entry.stem)
                logging.info(f"更新打包目标: {v}")
