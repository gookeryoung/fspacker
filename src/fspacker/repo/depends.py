import dataclasses
import logging
import typing

__all__ = ("fetch_depends_tree",)

import rtoml

from fspacker.config import MAX_SHOWN_FILES
from fspacker.dirs import get_depends_filepath


@dataclasses.dataclass
class DependsInfo:
    name: str
    files: typing.List[str]
    folders: typing.List[str]
    depends: typing.List[str]

    def __repr__(self):
        if len(self.files) >= MAX_SHOWN_FILES:
            files = [*self.files[:MAX_SHOWN_FILES], "..."]
        else:
            files = self.files
        return f"[name={self.name}, files={files}, \
            folders={self.folders}], depends={self.depends}"


_depends_config: typing.Dict[str, DependsInfo] = {}


def fetch_depends_tree() -> typing.Dict[str, DependsInfo]:
    global _depends_config

    if not len(_depends_config):
        depends: typing.Dict[str, DependsInfo] = {}
        config_file = get_depends_filepath()
        config = rtoml.load(config_file)
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
        _depends_config.update(depends)
        logging.info(f"获取依赖信息: {_depends_config}")

    return _depends_config
