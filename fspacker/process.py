import pathlib
import typing

from fspacker.core.parsers import parser_factory
from fspacker.packers.base import BasePacker
from fspacker.packers.depends import DependsPacker
from fspacker.packers.entry import EntryPacker
from fspacker.packers.library import LibraryPacker
from fspacker.packers.runtime import RuntimePacker


class Processor:
    def __init__(
        self,
        root_dir: pathlib.Path,
        file: typing.Optional[pathlib.Path] = None,
    ):
        self.root = root_dir
        self.file = file
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
        entries = sorted(
            list(_ for _ in self.root.iterdir() if self._check_entry(_)),
            key=lambda x: x.is_dir(),
        )

        for entry in entries:
            parser_factory.parse(entry, root_dir=self.root)

        for target in parser_factory.TARGETS.values():
            for packer in self.packers.values():
                packer.pack(target)
