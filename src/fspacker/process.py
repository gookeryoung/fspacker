import pathlib

from fspacker.common import BuildConfig
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

    def run(self):
        entries = sorted(list(self.root.iterdir()), key=lambda x: x.is_dir())
        for entry in entries:
            if entry.is_dir():
                self.parsers.get("folder").parse(entry)
            elif entry.is_file() and entry.suffix in ".py":
                self.parsers.get("source").parse(entry)
