import logging
import shutil

from fspacker.core.target import PackTarget
from fspacker.packers.base import BasePacker

__all__ = [
    "DependsPacker",
]


class DependsPacker(BasePacker):
    def pack(self, target: PackTarget):
        dst = target.dist_dir / "src"
        dst.mkdir(exist_ok=True, parents=True)

        root = target.root_dir
        logging.info(
            f"Copy source file: [{target.src.name}]->[{dst.relative_to(root)}]"
        )
        shutil.copy(str(target.src), str(dst))

        for dep in target.sources:
            dep_target = list(_ for _ in target.src.parent.glob(f"{dep}*"))[0]
            if dep_target.is_dir():
                shutil.copytree(
                    dep_target, str(dst / dep_target.stem), dirs_exist_ok=True
                )
            elif dep_target.is_file():
                shutil.copy(dep_target, str(dst / dep_target.name))
