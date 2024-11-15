import pathlib

from fspacker.common import BuildConfig
from fspacker.packer.base import BasePacker
from fspacker.packer.depends import DependsPacker
from fspacker.packer.entry import EntryPacker
from fspacker.packer.library import LibraryPacker
from fspacker.packer.runtime import RuntimePacker
from fspacker.parser.folder import FolderParser
from fspacker.parser.source import SourceParser


class Processor:
    def __init__(self, root_dir: pathlib.Path):
        self.config = BuildConfig(targets={})
        self.root = root_dir
        self.parsers = dict(
            source=SourceParser(self.config, root_dir),
            folder=FolderParser(self.config, root_dir),
        )
        self.packers = dict(
            base=BasePacker(),
            entry=EntryPacker(),
            runtime=RuntimePacker(),
            depends=DependsPacker(),
            library=LibraryPacker(),
        )

    def run(self):
        entries = sorted(list(self.root.iterdir()), key=lambda x: x.is_dir())
        for entry in entries:
            if entry.is_dir():
                self.parsers.get("folder").parse(entry)
            elif entry.is_file() and entry.suffix in ".py":
                self.parsers.get("source").parse(entry)

        for target in self.config.targets.values():
            for packer in self.packers.values():
                packer.pack(target)
