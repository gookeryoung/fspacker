import typing

from fspacker.common import PackTarget
from fspacker.utils.wheel import unpack_wheel


class LibSpecPackerMixin:
    PATTERNS: typing.Dict[str, typing.Set[str]] = {}

    def pack(self, lib: str, target: PackTarget):
        for libname, patterns in self.PATTERNS.items():
            unpack_wheel(libname.lower(), target.packages_dir, patterns)


class BaseLibrarySpecPacker:
    def pack(self, lib: str, target: PackTarget):
        pass


class DefaultLibrarySpecPacker(BaseLibrarySpecPacker):
    def pack(self, lib: str, target: PackTarget):
        unpack_wheel(lib, target.packages_dir, {})
