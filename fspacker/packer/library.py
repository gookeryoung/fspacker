import logging

from fspacker.common import BuildTarget
from fspacker.packer.base import BasePacker
from fspacker.packer.libspec.base import BaseLibrarySpecPacker
from fspacker.packer.libspec.gui import PySide2Packer
from fspacker.packer.libspec.tkinter import TkinterPacker

__all__ = [
    "LibraryPacker",
]


class LibraryPacker(BasePacker):
    def __init__(self):
        super().__init__()

        self.spec_packers = dict(
            tkinter=TkinterPacker(),
            pyside2=PySide2Packer(),
        )

    def pack(self, target: BuildTarget):
        packages_dir = target.packages_dir

        if not packages_dir.exists():
            logging.info(f"创建包目录[{packages_dir}]")
            packages_dir.mkdir(parents=True)

        for libname in target.ast:
            self.spec_packers.setdefault(libname, BaseLibrarySpecPacker()).pack(target=target)
