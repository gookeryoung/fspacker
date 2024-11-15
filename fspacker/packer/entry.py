import logging
import shutil
import string

from fspacker.common import PackTarget
from fspacker.config import GUI_LIBS, ASSETS_DIR
from fspacker.packer.base import BasePacker

# int file template
INT_TEMPLATE = string.Template(
    """\
import sys, os
sys.path.append(os.path.join(os.getcwd(), "src"))
from $SRC import main
main()
"""
)


class EntryPacker(BasePacker):
    def pack(self, target: PackTarget):
        is_gui = target.ast.union(target.extra).intersection(GUI_LIBS)

        exe_file = "gui.exe" if is_gui else "console.exe"
        src = ASSETS_DIR / exe_file
        dst = target.dist_dir / f"{target.src.stem}.exe"

        if not dst.exists():
            logging.info(f"Target is [{'GUI' if is_gui else 'CONSOLE'}]")
            logging.info(f"Copy executable file: [{src}]->[{dst}]")
            shutil.copy(src, dst)
        else:
            logging.info(f"Entry file [{dst.relative_to(target.root_dir)}] already exist, skip")

        name = target.src.stem
        dst = target.dist_dir / f"{name}.int"

        logging.info(f"Create int file: [{name}.int]->[{dst.relative_to(target.root_dir)}]")
        content = INT_TEMPLATE.substitute(SRC=f"src.{name}")
        with open(dst, "w") as f:
            f.write(content)
