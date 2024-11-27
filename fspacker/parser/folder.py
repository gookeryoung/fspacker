import logging
import pathlib

from fspacker.config import IGNORE_SYMBOLS
from fspacker.parser.base import BaseParser


class FolderParser(BaseParser):
    """Parser for folders"""

    def parse(self, entry: pathlib.Path):
        if entry.stem.lower() in IGNORE_SYMBOLS:
            logging.info(f"Skip parsing folder: [{entry.stem}]")
            return

        for k, v in self.targets.items():
            if entry.stem in v.code:
                v.deps.add(entry.stem)
                logging.info(f"Update pack target: {v}")
