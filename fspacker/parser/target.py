import dataclasses
import pathlib
import typing
from functools import cached_property


__all__ = ["Dependency", "PackTarget"]


@dataclasses.dataclass
class Dependency:
    """Dependency data of the project, including:

    Attributes
    ----------
    libs: typing.Set[str]
        External libraries.
    sources: typing.Set[str]
        Source files and folders.
    extra: typing.Set[str]
        Extra specific info.
    """

    libs: typing.Set[str]
    sources: typing.Set[str]
    extra: typing.Set[str]

    __slots__ = ("libs", "sources", "extra")

    def __init__(self):
        self.libs = set()
        self.sources = set()
        self.extra = set()


@dataclasses.dataclass
class PackTarget:
    src: pathlib.Path
    depends: Dependency
    code: str

    def __repr__(self):
        return f"[src={self.src.name}, sources={self.sources}, libs={self.sources}], extra={self.extra}"

    @property
    def sources(self):
        return self.depends.sources

    @property
    def libs(self):
        return self.depends.libs

    @property
    def extra(self):
        return self.depends.extra

    @cached_property
    def root_dir(self) -> pathlib.Path:
        return self.src.parent

    @cached_property
    def dist_dir(self) -> pathlib.Path:
        return self.src.parent / "dist"

    @cached_property
    def runtime_dir(self) -> pathlib.Path:
        return self.dist_dir / "runtime"

    @cached_property
    def packages_dir(self) -> pathlib.Path:
        return self.dist_dir / "site-packages"
