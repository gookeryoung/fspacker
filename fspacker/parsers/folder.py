import logging
import pathlib

from fspacker.parsers.base import BaseParser
from fspacker.settings import settings


class FolderParser(BaseParser):
    """Parser for folders"""

    def parse(self, entry: pathlib.Path):
        if entry.stem.lower() in settings.IGNORE_SYMBOLS:
            logging.info(f"Skip parsing folder: [{entry.stem}]")
            return

        for k, v in self.targets.items():
            if entry.stem in v.code:
                v.sources.add(entry.stem)
                logging.info(f"Update pack target: {v}")
