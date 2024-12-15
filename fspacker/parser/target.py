import dataclasses
import pathlib
import typing
from functools import cached_property


__all__ = [
    "DependInfo",
    "PackTarget"
]


@dataclasses.dataclass
class DependInfo:
    deps: typing.Set[str]
    ast: typing.Set[str]
    extra: typing.Set[str]

    def __init__(self):
        self.deps = set()
        self.ast = set()
        self.extra = set()

    def __or__(self, other):
        if not isinstance(other, DependInfo):
            raise ValueError(f"object {other} is not instance of DependInfo")

        self.deps |= other.deps
        self.ast |= other.ast
        self.extra |= other.extra

    def __ior__(self, other):
        if not isinstance(other, DependInfo):
            raise ValueError(f"object {other} is not instance of DependInfo")

        self.deps |= other.deps
        self.ast |= other.ast
        self.extra |= other.extra


@dataclasses.dataclass
class PackTarget:
    src: pathlib.Path
    deps: typing.Set[str]
    ast: typing.Set[str]
    extra: typing.Set[str]
    code: str

    def __repr__(self):
        return f"[src={self.src.name}, ast={self.ast}, deps={self.deps}], extra={self.extra}"

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
