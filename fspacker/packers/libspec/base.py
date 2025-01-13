import logging
import typing

from fspacker.core.archive import unpack
from fspacker.core.resources import resources
from fspacker.core.target import PackTarget
from fspacker.packers.base import BasePacker
from fspacker.utils.libs import install_lib


class LibSpecPackerMixin:
    PATTERNS: typing.Dict[str, typing.Set[str]] = {}
    EXCLUDES: typing.Dict[str, typing.Set[str]] = {}

    def pack(self, lib: str, target: PackTarget):
        pass

    @property
    def info(self):
        return f"EXCLUDES={set(self.EXCLUDES.keys())}, PATTERNS={set(self.PATTERNS.keys())}"


class ChildLibSpecPacker(LibSpecPackerMixin):
    def __init__(self, parent: BasePacker) -> None:
        self.parent = parent

    def pack(self, lib: str, target: PackTarget):
        specs = {k: v for k, v in self.parent.SPECS.items() if k != lib}

        logging.info(f"Use [{self.__class__.__name__}] spec, {self.info}")
        if len(self.PATTERNS):
            for libname, patterns in self.PATTERNS.items():
                if libname in specs:
                    specs[libname].pack(libname, target=target)
                else:
                    excludes = self.EXCLUDES.setdefault(libname, set())
                    install_lib(libname, target, patterns, excludes)
        else:
            excludes = self.EXCLUDES.setdefault(lib, set())
            install_lib(lib, target, excludes=excludes)


class DefaultLibrarySpecPacker(LibSpecPackerMixin):
    def pack(self, lib: str, target: PackTarget):
        if lib not in target.lib_folders:
            logging.info(f"Packing [{lib}], using [default] lib spec")
            info = resources.LIBS_REPO.get(lib)
            if info.filepath.suffix == ".whl":
                install_lib(lib, target)
            elif info.filepath.suffix == ".gz":
                unpack(info.filepath, target.packages_dir)
            else:
                logging.error(f"[!!!] Lib {lib} not found!")
        else:
            logging.info(f"Already packed, skip [{lib}]")
