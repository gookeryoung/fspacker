import dataclasses
import logging
import typing

__all__ = ("fetch_depends_tree",)

import rtoml

from fspacker.dirs import get_depends_filepath


@dataclasses.dataclass
class DependsInfo:
    name: str
    files: typing.List[str]
    folders: typing.List[str]

    def __repr__(self):
        return f"[name={self.name}, files={self.files}, folders={self.folders}]"


_depends_config: typing.Dict[str, DependsInfo] = {}


def fetch_depends_tree() -> typing.Dict[str, DependsInfo]:
    global _depends_config

    if not len(_depends_config):
        depends = {}
        config_file = get_depends_filepath()
        config = rtoml.load(config_file)
        for k, v in config.items():
            depends.setdefault(
                k,
                DependsInfo(
                    name=k,
                    files=config[k]["files"],
                    folders=config[k]["folders"],
                ),
            )
        _depends_config.update(depends)
        logging.info(f"获取依赖信息: {_depends_config}")

    return _depends_config
