import logging

from fspacker.packer.base import BasePacker
from fspacker.packer.libspec.base import DefaultLibrarySpecPacker
from fspacker.packer.libspec.gui import (
    PySide2Packer,
    PygamePacker,
    TkinterPacker,
)
from fspacker.packer.libspec.sci import (
    MatplotlibSpecPacker,
    NumbaSpecPacker,
    PandasSpecPacker,
    TorchSpecPacker,
)
from fspacker.parser.target import PackTarget
from fspacker.utils.libs import get_lib_meta_depends
from fspacker.utils.repo import get_libs_repo, update_libs_repo, map_libname
from fspacker.utils.wheel import download_wheel

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
            pandas=PandasSpecPacker(self),
            torch=TorchSpecPacker(self),
        )
        self.libs_repo = get_libs_repo()

    def _update_lib_depends(
        self, lib_name: str, target: PackTarget, depth: int
    ):
        lib_name = map_libname(lib_name)
        lib_info = self.libs_repo.get(lib_name)
        if lib_info is None:
            filepath = download_wheel(lib_name)
            if filepath and filepath.exists():
                update_libs_repo(lib_name, filepath)
        else:
            filepath = lib_info.filepath

        if filepath and filepath.exists():
            lib_depends = get_lib_meta_depends(filepath)
            target.depends.libs |= lib_depends

            # if depth <= self.MAX_DEPEND_DEPTH:
            #     for lib_depend in lib_depends:
            #         self._update_lib_depends(lib_depend, target, depth + 1)

    def pack(self, target: PackTarget):
        for lib in set(target.libs):
            self._update_lib_depends(lib, target, 0)

        logging.info(f"After updating target ast tree: {target}")
        logging.info("Start packing with specs")
        for k, v in self.SPECS.items():
            if k in target.libs:
                self.SPECS[k].pack(k, target=target)
                target.libs.remove(k)

            if k in target.extra:
                self.SPECS[k].pack(k, target=target)

        logging.info("Start packing with default")
        for lib in target.libs:
            lib = map_libname(lib)
            if lib in self.libs_repo.keys():
                self.SPECS["default"].pack(lib, target=target)
            else:
                logging.error(
                    f"[!!!] Lib [{lib}] for [{lib}] not found in repo"
                )
