import logging
import shutil
import string

from fspacker.dirs import get_dist_dir, get_assets_dir
from fspacker.parser.source import SourceParser

__all__ = ("pack_entry",)

# int 文件模板
TEMPLATE = string.Template(
    """\
import sys, os
sys.path.append(os.path.join(os.getcwd(), "src"))
from $SRC import main
main()
"""
)


def _pack_int_file(parser: SourceParser) -> None:
    name = parser.config.project_name
    dst = get_dist_dir(parser.directory) / f"{name}.int"

    logging.info(f"创建int文件[{name}.int]->[{dst}]")
    content = TEMPLATE.substitute(SRC=f"src.{name}")
    with open(dst, "w") as f:
        f.write(content)


def pack_entry(parser: SourceParser) -> None:
    name = parser.config.project_name
    exe_file = "gui.exe" if parser.config.is_gui else "console.exe"
    src = get_assets_dir() / exe_file
    dst = (get_dist_dir(parser.directory) / exe_file).with_name(f"{name}.exe")

    if not dst.exists():
        logging.info(
            f"分析为[{'窗体' if parser.config.is_gui else '控制台'}]目标"
        )
        logging.info(f"拷贝可执行文件[{src}]->[{dst}]")
        shutil.copy(src, dst)
    else:
        logging.info(f"入口文件[{dst}]已存在, 跳过")

    _pack_int_file(parser)
