import pathlib
import typing

from fspacker.parsers.target import PackTarget


class BaseParser:
    """Base class for parsers"""

    def __init__(
        self,
        root_dir: pathlib.Path,
        targets: typing.Dict[str, PackTarget] = None,
    ):
        self.targets = targets if targets is not None else {}
        self.root = root_dir

    def parse(self, entry: pathlib.Path):
        pass
