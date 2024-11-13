import logging
import shutil

from fspacker.common import BuildTarget
from fspacker.dirs import get_dist_dir
from fspacker.packer.base import BasePacker


class DependsPacker(BasePacker):
    def pack(self, target: BuildTarget):
        dst = get_dist_dir(target.src.parent) / "src"
        dst.mkdir(exist_ok=True, parents=True)

        logging.info(f"复制源文件[{target.src}]->[{dst}]")
        shutil.copy(str(target.src), str(dst))

        for dep in target.deps:
            dep_target = list(_ for _ in target.src.parent.glob(f"{dep}*"))[0]
            if dep_target.is_dir():
                shutil.copytree(
                    dep_target, str(dst / dep_target.stem), dirs_exist_ok=True
                )
            elif dep_target.is_file():
                shutil.copy(dep_target, str(dst / dep_target.name))
