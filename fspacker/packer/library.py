import logging

from fspacker.packer.base import BasePacker
from fspacker.packer.libspec.base import DefaultLibrarySpecPacker
from fspacker.packer.libspec.gui import PySide2Packer, TkinterPacker
from fspacker.packer.libspec.sci import (
    MatplotlibSpecPacker,
    TorchSpecPacker,
)
from fspacker.parser.target import PackTarget
from fspacker.utils.repo import get_libs_repo, update_libs_repo, map_libname
from fspacker.utils.wheel import download_wheel, get_dependencies

__all__ = [
    "LibraryPacker",
]


class LibraryPacker(BasePacker):
    def __init__(self):
        super().__init__()

        self.SPECS = dict(
            default=DefaultLibrarySpecPacker(),
            # gui
            pyside2=PySide2Packer(self),
            tkinter=TkinterPacker(self),
            # sci
            matplotlib=MatplotlibSpecPacker(self),
            torch=TorchSpecPacker(self),
        )

    def pack(self, target: PackTarget):
        libs_repo = get_libs_repo()

        for lib in set(target.libs):
            lib = map_libname(lib)
            lib_info = libs_repo.get(lib)
            if lib_info is None:
                filepath = download_wheel(lib)
                if filepath.exists():
                    update_libs_repo(lib, filepath)
            else:
                filepath = lib_info.filepath

            ast_tree = get_dependencies(filepath, 0)
            target.depends.libs |= ast_tree

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
            real_libname = map_libname(lib)
            if real_libname in libs_repo.keys():
                self.SPECS["default"].pack(real_libname, target=target)
