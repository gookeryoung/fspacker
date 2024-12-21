import atexit
import json
import logging
import pathlib
import typing
from collections import UserDict

from fspacker.config import CONFIG_FILEPATH

__all__ = [
    "ConfigManager",
    "get_config_manager",
]


class ConfigManager(UserDict):
    def __init__(self, config_file: pathlib.Path, default_config=None):
        super().__init__()

        self.config_file = config_file
        self.config = default_config or {}
        if self.config_file and self.config_file.exists():
            self.load()
        else:
            logging.error(
                f"[!!!] File [{self.config_file.name}] doesn't exist."
            )
            return

    def load(self):
        logging.info(f"Load logging file: [{self.config_file.name}]")
        with open(self.config_file) as f:
            self.config.update(json.load(f))

    def save(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, ensure_ascii=True, indent=4)

    def __setitem__(self, key, value):
        self.config[key] = value

    def __getitem__(self, key):
        try:
            return self.config.get(key)
        except KeyError:
            logging.info(f"Key [{key}] not in [{self.config}]")
            return None


__global_config: typing.Optional[ConfigManager] = None


def get_config_manager():
    global __global_config

    if __global_config is None:
        __global_config = ConfigManager(CONFIG_FILEPATH)
    return __global_config


atexit.register(get_config_manager().save)
