import logging
import shutil

from fspacker.conf.settings import settings
from fspacker.core.target import PackTarget
from fspacker.packers.libspec.base import ChildLibSpecPacker


class PySide2Packer(ChildLibSpecPacker):
    PATTERNS = dict(
        pyside2={
            "PySide2/__init__.py",
            "PySide2/pyside2.abi3.dll",
            "PySide2/QtCore.pyd",
            "PySide2/Qt5Core.dll",
            "PySide2/QtGui.pyd",
            "PySide2/Qt5Gui.dll",
            "PySide2/QtWidgets.pyd",
            "PySide2/Qt5Widgets.dll",
            "PySide2/QtNetwork.pyd",
            "PySide2/Qt5Network.dll",
            "PySide2/QtQml.pyd",
            "PySide2/Qt5Qml.dll",
            "*plugins/iconengines/qsvgicon.dll",
            "*plugins/imageformats/*.dll",
            "*plugins/platforms/*.dll",
        },
    )


class PygamePacker(ChildLibSpecPacker):
    EXCLUDES = dict(
        pygame={
            "pygame/docs/*",
            "pygame/examples/*",
            "pygame/tests/*",
            "pygame/__pyinstaller/*",
            "pygame*data/*",
        },
    )


class TkinterPacker(ChildLibSpecPacker):
    def pack(self, lib: str, target: PackTarget):
        if "tkinter" in target.extra:
            logging.info("Use [tkinter] pack spec")

            if not (target.dist_dir / "lib").exists():
                logging.info(
                    f"Unpacking tkinter: [{settings.tkinter_lib_path.name}]->[{target.packages_dir.name}]"
                )
                shutil.unpack_archive(settings.tkinter_lib_path, target.dist_dir, "zip")
            else:
                logging.info("[tkinter][lib] already packed, skipping")

            if not (target.packages_dir / "tkinter").exists():
                shutil.unpack_archive(settings.tkinter_path, target.packages_dir, "zip")
            else:
                logging.info("[tkinter][packages] already packed, skipping")
