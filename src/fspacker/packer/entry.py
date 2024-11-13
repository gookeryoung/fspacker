import logging
import shutil
import string

from fspacker.common import BuildTarget
from fspacker.config import GUI_LIBS
from fspacker.dirs import get_assets_dir, get_dist_dir
from fspacker.packer.base import BasePacker

# int 文件模板
TEMPLATE = string.Template(
    """\
import sys, os
sys.path.append(os.path.join(os.getcwd(), "src"))
from $SRC import main
main()
"""
)


class EntryPacker(BasePacker):
    def pack(self, target: BuildTarget):
        is_gui = target.ast.intersection(GUI_LIBS)

        exe_file = "gui.exe" if is_gui else "console.exe"
        src = get_assets_dir() / exe_file
        dst = get_dist_dir(target.src.parent) / f"{target.src.stem}.exe"

        if not dst.exists():
            logging.info(f"分析为[{'窗体' if is_gui else '控制台'}]目标")
            logging.info(f"拷贝可执行文件[{src}]->[{dst}]")
            shutil.copy(src, dst)
        else:
            logging.info(f"入口文件[{dst}]已存在, 跳过")

        name = target.src.stem
        dst = get_dist_dir(target.src.parent) / f"{name}.int"

        logging.info(f"创建int文件[{name}.int]->[{dst}]")
        content = TEMPLATE.substitute(SRC=f"src.{name}")
        with open(dst, "w") as f:
            f.write(content)
