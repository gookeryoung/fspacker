import pathlib
import typing

from fspacker.parser.target import PackTarget


class BaseParser:
    """Base class for parsers"""

    def __init__(self, targets: typing.Dict[str, PackTarget], root_dir: pathlib.Path):
        self.targets = targets
        self.root = root_dir

    def parse(self, entry: pathlib.Path): ...
