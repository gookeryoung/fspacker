import dataclasses
import pathlib
import typing
from functools import cached_property


@dataclasses.dataclass
class PackTarget:
    src: pathlib.Path
    deps: typing.Set[str]
    ast: typing.Set[str]
    extra: typing.Set[str]
    code: str

    def __repr__(self):
        return f"[src={self.src.name}, ast={self.ast}, deps={self.deps}], extra={self.extra}"

    def union_ast(self, ast_tree: typing.Set[str]):
        self.ast = self.ast.union(ast_tree)

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
