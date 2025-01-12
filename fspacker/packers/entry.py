import logging
import shutil
import string

from fspacker.conf.settings import settings
from fspacker.core.target import PackTarget
from fspacker.packers.base import BasePacker

# int file template
INT_TEMPLATE = string.Template(
    """\
import sys, os
sys.path.append(os.path.join(os.getcwd(), "src"))
from $SRC import main
main()
"""
)

INT_TEMPLATE_QT = string.Template(
    """\
import sys, os
import PySide2

qt_dir = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(qt_dir, "plugins" , "platforms")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
sys.path.append(os.path.join(os.getcwd(), "src"))
from $SRC import main
main()
"""
)


class EntryPacker(BasePacker):
    def pack(self, target: PackTarget):
        is_gui = target.libs.union(target.extra).intersection(settings.gui_libs)

        exe_file = "gui.exe" if is_gui else "console.exe"
        src = settings.assets_dir / exe_file
        root = target.root_dir
        dst = target.dist_dir / f"{target.src.stem}.exe"

        if not dst.exists():
            logging.info(f"Target is [{'GUI' if is_gui else 'CONSOLE'}]")
            logging.info(
                f"Copy executable file: [{src.name}]->[{dst.relative_to(root)}]"
            )
            shutil.copy(src, dst)
        else:
            logging.info(f"Entry file [{dst.relative_to(root)}] already exist, skip")

        name = target.src.stem
        dst = target.dist_dir / f"{name}.int"

        logging.info(f"Create int file: [{name}.int]->[{dst.relative_to(root)}]")
        if {"pyside2", "pyside6", "pyqt5", "pyqt6"}.intersection(
            set(x.lower() for x in target.libs)
        ):
            content = INT_TEMPLATE_QT.substitute(SRC=f"src.{name}")
        else:
            content = INT_TEMPLATE.substitute(SRC=f"src.{name}")

        with open(dst, "w") as f:
            f.write(content)
