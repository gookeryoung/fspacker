import atexit
import json
import logging
import pathlib
import typing
from collections import UserDict

from fspacker.config import CONFIG_FILEPATH

__all__ = [
    "ConfigManager",
]


class ConfigManager(UserDict):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        super().__init__()

        if not hasattr(self, "initialized"):
            self.initialized = True

            self.config_file = CONFIG_FILEPATH
            self.config = {}

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


atexit.register(ConfigManager().save)
