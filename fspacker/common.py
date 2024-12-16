import dataclasses
import pathlib

from pkginfo import Distribution

__all__ = [
    "LibraryInfo",
]


@dataclasses.dataclass
class LibraryInfo:
    meta_data: Distribution
    filepath: pathlib.Path

    def __repr__(self):
        return f"{self.meta_data.name}-{self.meta_data.version}"
