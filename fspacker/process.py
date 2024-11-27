import pathlib

from fspacker.packer.base import BasePacker
from fspacker.packer.depends import DependsPacker
from fspacker.packer.entry import EntryPacker
from fspacker.packer.library import LibraryPacker
from fspacker.packer.runtime import RuntimePacker
from fspacker.parser.folder import FolderParser
from fspacker.parser.source import SourceParser
from fspacker.parser.target import PackTarget


class Processor:
    def __init__(self, root_dir: pathlib.Path):
        self.targets: typing.Set[PackTarget] = {}
        self.root = root_dir
        self.parsers = dict(
            source=SourceParser(self.targets, root_dir),
            folder=FolderParser(self.targets, root_dir),
        )
        self.packers = dict(
            base=BasePacker(),
            depends=DependsPacker(),
            entry=EntryPacker(),
            runtime=RuntimePacker(),
            library=LibraryPacker(),
        )

    def run(self):
        entries = sorted(list(self.root.iterdir()), key=lambda x: x.is_dir())
        for entry in entries:
            if entry.is_dir():
                self.parsers.get("folder").parse(entry)
            elif entry.is_file() and entry.suffix in ".py":
                self.parsers.get("source").parse(entry)

        for target in self.targets.values():
            for packer in self.packers.values():
                packer.pack(target)
