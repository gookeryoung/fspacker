import logging

from fspacker.packer.base import BasePacker
from fspacker.packer.libspec.base import DefaultLibrarySpecPacker
from fspacker.packer.libspec.gui import PySide2Packer, TkinterPacker
from fspacker.packer.libspec.sci import (
    MatplotlibSpecPacker,
    TorchSpecPacker,
)
from fspacker.parser.target import PackTarget
from fspacker.utils.repo import get_libs_repo, update_libs_repo
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

        for lib in target.ast:
            lib_info = libs_repo.get(lib)
            if lib_info is None:
                filepath = download_wheel(lib)
                if filepath.exists():
                    update_libs_repo(lib, filepath)

            ast_tree = get_dependencies(lib, 0)
            target.union_ast(ast_tree)

        logging.info(f"After updating target ast tree: {target}")
        logging.info("Start packing with specs")
        for k, v in self.SPECS.items():
            if k in target.ast:
                self.SPECS[k].pack(k, target=target)
                target.ast.remove(k)

            if k in target.extra:
                self.SPECS[k].pack(k, target=target)

        logging.info("Start packing with default")
        for lib in target.ast:
            if lib in libs_repo.keys():
                self.SPECS["default"].pack(lib, target=target)
