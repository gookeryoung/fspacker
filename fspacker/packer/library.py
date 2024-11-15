import logging

from fspacker.common import PackTarget
from fspacker.packer.base import BasePacker
from fspacker.packer.libspec.base import DefaultLibrarySpecPacker
from fspacker.packer.libspec.gui import PySide2Packer, TkinterPacker

__all__ = [
    "LibraryPacker",
]

from fspacker.utils.repo import get_libs_repo
from fspacker.utils.wheel import download_install_wheel


class LibraryPacker(BasePacker):
    def __init__(self):
        super().__init__()

        self.spec_packers = dict(
            tkinter=TkinterPacker(),
            pyside2=PySide2Packer(),
        )

    def pack(self, target: PackTarget):
        packages_dir = target.packages_dir
        libs_repo = get_libs_repo()

        if not packages_dir.exists():
            logging.info(f"Create packages folder [{packages_dir}]")
            packages_dir.mkdir(parents=True)

        for libname in target.ast:
            if not libs_repo.get(libname):
                download_install_wheel(libname, packages_dir)
            else:
                self.spec_packers.setdefault(libname, DefaultLibrarySpecPacker()).pack(libname, target=target)
