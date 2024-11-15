import logging
import shutil

from fspacker.common import PackTarget
from fspacker.config import TKINTER_LIB_FILEPATH, TKINTER_FILEPATH
from fspacker.packer.libspec.base import ChildLibSpecPacker


class PySide2Packer(ChildLibSpecPacker):
    PATTERNS = dict(
        pyside2={
            "PySide2/__init__.py",
            "PySide2/pyside2.abi3.dll",
            "PySide2/Qt5?Core",
            "PySide2/Qt5?Gui",
            "PySide2/Qt5?Widgets",
            "PySide2/Qt5?Network.dll",
            "PySide2/Qt5?Network.py.*",
            "PySide2/Qt5?Qml.dll",
            "PySide2/Qt5?Qml.py.*",
            "plugins/iconengines/qsvgicon.dll",
            "plugins/imageformats/.*.dll",
            "plugins/platforms/.*.dll",
        },
        shiboken2=set(),
        six=set(),
    )

    def pack(self, lib: str, target: PackTarget):
        logging.info("Using [pyside2] pack spec")
        super().pack(lib, target)


class TkinterPacker(ChildLibSpecPacker):
    def pack(self, lib: str, target: PackTarget):
        if "tkinter" in target.extra:
            logging.info("Using [tkinter] pack spec")
            shutil.unpack_archive(TKINTER_LIB_FILEPATH, target.dist_dir, "zip")
            shutil.unpack_archive(TKINTER_FILEPATH, target.packages_dir, "zip")
