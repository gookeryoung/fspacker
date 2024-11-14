import logging
import shutil
import typing

import rtoml

from fspacker.common import BuildTarget, DependsInfo
from fspacker.config import DEPENDS_FILEPATH
from fspacker.packer.base import BasePacker

__all__ = [
    "parse_depends_tree",
    "DependsPacker",
]

__depends_repo: typing.Dict[str, DependsInfo] = {}


def parse_depends_tree() -> typing.Dict[str, DependsInfo]:
    global __depends_repo

    if not len(__depends_repo):
        depends: typing.Dict[str, DependsInfo] = {}
        config = rtoml.load(DEPENDS_FILEPATH)
        for k, v in config.items():
            depends.setdefault(
                k.lower(),
                DependsInfo(
                    name=k,
                    files=config[k].get("files"),
                    folders=config[k].get("folders"),
                    depends=config[k].get("depends"),
                ),
            )
        __depends_repo.update(depends)
        logging.info(f"获取依赖信息: {__depends_repo}")

    return __depends_repo


class DependsPacker(BasePacker):
    def pack(self, target: BuildTarget):
        dst = target.dist_dir / "src"
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

