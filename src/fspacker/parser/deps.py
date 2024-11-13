import logging
import shutil

from fspacker.dirs import get_dist_dir
from fspacker.common import BuildTarget

__all__ = ("pack_src_deps",)


def pack_src_deps(target: BuildTarget):
    dst = get_dist_dir(target.src.parent) / "src"
    dst.mkdir(exist_ok=True, parents=True)

    logging.info(f"复制源文件[{target.src}]->[{dst}]")
    shutil.copy(str(target.src), str(dst))

    for dep in target.deps:
        if dep.is_dir():
            shutil.copytree(dep, str(dst / dep.stem), dirs_exist_ok=True)
        elif dep.is_file():
            shutil.copy(dep, str(dst / dep.name))
