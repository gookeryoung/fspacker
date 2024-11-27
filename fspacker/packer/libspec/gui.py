import logging
import shutil

from fspacker.config import TKINTER_FILEPATH, TKINTER_LIB_FILEPATH
from fspacker.packer.libspec.base import ChildLibSpecPacker
from fspacker.parser.target import PackTarget


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
    )


class TkinterPacker(ChildLibSpecPacker):
    def pack(self, lib: str, target: PackTarget):
        if "tkinter" in target.extra:
            logging.info("Use [tkinter] pack spec")

            if not (target.dist_dir / "lib").exists():
                logging.info(
                    f"Unpacking tkinter: [{TKINTER_FILEPATH.name}]->[{target.packages_dir.name}]"
                )
                shutil.unpack_archive(TKINTER_LIB_FILEPATH, target.dist_dir, "zip")
            else:
                logging.info("[tkinter][lib] already packed, skipping")

            if not (target.packages_dir / "tkinter").exists():
                shutil.unpack_archive(TKINTER_FILEPATH, target.packages_dir, "zip")
            else:
                logging.info("[tkinter][packages] already packed, skipping")
