import typing

from fspacker.common import BuildTarget
from fspacker.utils.wheel import unzip_wheel


class LibSpecPackerMixin:
    PATTERNS: typing.Dict[str, typing.Set[str]] = {}

    def pack(self, lib: str, target: BuildTarget):
        for libname, patterns in self.PATTERNS.items():
            unzip_wheel(libname.lower(), target.packages_dir, patterns)


class BaseLibrarySpecPacker:
    def pack(self, lib: str, target: BuildTarget):
        pass


class DefaultLibrarySpecPacker(BaseLibrarySpecPacker):
    def pack(self, lib: str, target: BuildTarget):
        unzip_wheel(lib, target.packages_dir, {})
