import pathlib

from fspacker.common import PackConfig


class BaseParser:
    """Base class for parsers"""

    def __init__(self, config: PackConfig, root_dir: pathlib.Path):
        self.config = config
        self.root = root_dir

    def parse(self, entry: pathlib.Path): ...
