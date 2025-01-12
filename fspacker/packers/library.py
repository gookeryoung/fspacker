import logging

from fspacker.core.libraries import get_libname
from fspacker.core.resources import resources
from fspacker.core.target import PackTarget
from fspacker.packers.base import BasePacker
from fspacker.packers.libspec.base import DefaultLibrarySpecPacker
from fspacker.packers.libspec.gui import (
    PySide2Packer,
    PygamePacker,
    TkinterPacker,
)
from fspacker.packers.libspec.sci import (
    MatplotlibSpecPacker,
    NumbaSpecPacker,
    NumpySpecPacker,
    PandasSpecPacker,
    TorchSpecPacker,
)
from fspacker.utils.libs import install_lib

__all__ = [
    "LibraryPacker",
]


class LibraryPacker(BasePacker):
    MAX_DEPEND_DEPTH = 0

    def __init__(self):
        super().__init__()

        self.SPECS = dict(
            default=DefaultLibrarySpecPacker(),
            # gui
            pyside2=PySide2Packer(self),
            pygame=PygamePacker(self),
            tkinter=TkinterPacker(self),
            # sci
            matplotlib=MatplotlibSpecPacker(self),
            numba=NumbaSpecPacker(self),
            numpy=NumpySpecPacker(self),
            pandas=PandasSpecPacker(self),
            torch=TorchSpecPacker(self),
        )

    def pack(self, target: PackTarget):
        for lib in set(target.libs):
            install_lib(lib, target, extend_depends=True)

        logging.info(f"After updating target ast tree: {target}")
        logging.info("Start packing with specs")
        for k, v in self.SPECS.items():
            if k in target.libs:
                self.SPECS[k].pack(k, target=target)
                target.libs.remove(k)
            if k in target.extra:
                self.SPECS[k].pack(k, target=target)

        logging.info(f"Start packing [{target.libs}] with default")
        for lib in list(target.libs):
            lib = get_libname(lib)
            if lib in resources.LIBS_REPO.keys():
                self.SPECS["default"].pack(lib, target=target)
            else:
                logging.error(f"[!!!] Lib [{lib}] for [{lib}] not found in repo")
                install_lib(lib, target)
