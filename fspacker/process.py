import pathlib
import typing

from fspacker.packer.base import BasePacker
from fspacker.packer.depends import DependsPacker
from fspacker.packer.entry import EntryPacker
from fspacker.packer.library import LibraryPacker
from fspacker.packer.runtime import RuntimePacker
from fspacker.parser.folder import FolderParser
from fspacker.parser.source import SourceParser
from fspacker.parser.target import PackTarget


class Processor:
    def __init__(
        self,
        root_dir: pathlib.Path,
        file: typing.Optional[pathlib.Path] = None,
    ):
        self.targets: typing.Dict[str, PackTarget] = {}
        self.root = root_dir
        self.file = file
        self.parsers = dict(
            source=SourceParser(root_dir, self.targets),
            folder=FolderParser(root_dir, self.targets),
        )
        self.packers = dict(
            base=BasePacker(),
            depends=DependsPacker(),
            entry=EntryPacker(),
            runtime=RuntimePacker(),
            library=LibraryPacker(),
        )

    @staticmethod
    def _check_entry(entry: pathlib.Path) -> bool:
        return any(
            (
                entry.is_dir(),
                entry.is_file() and entry.suffix in ".py",
            )
        )

    def run(self):
        if self.file:
            entries = [self.file]
        else:
            entries = sorted(
                list(_ for _ in self.root.iterdir() if self._check_entry(_)),
                key=lambda x: x.is_dir(),
            )

        for entry in entries:
            if entry.is_dir():
                self.parsers.get("folder").parse(entry)
            elif entry.is_file() and entry.suffix in ".py":
                self.parsers.get("source").parse(entry)

        for target in self.targets.values():
            for packer in self.packers.values():
                packer.pack(target)
