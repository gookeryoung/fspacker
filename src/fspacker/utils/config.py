import atexit
import logging
import pathlib
import typing
from collections import UserDict

import rtoml

from fspacker.config import CACHE_DIR


class ConfigManager(UserDict):
    _instance = None

    file_path: pathlib.Path = CACHE_DIR / "config.toml"

    def __new__(cls, filepath: str = ""):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            if filepath:
                cls.file_path = pathlib.Path(filepath)

            if not cls.file_path.exists():
                cls._instance.data = {}
                logging.error(f"[!!!] Config file [{cls.file_path}] not exists.")
            else:
                cls._instance.data = rtoml.load(cls.file_path)
        return cls._instance

    def __repr__(self):
        return f"ConfigManager: {self.data}"

    def __missing__(self, key: str):
        if isinstance(key, str):
            return KeyError(key)
        return self[str(key)]

    def __setitem__(self, key: str, value: typing.Any) -> None:
        """Set a value in the config by key. Key can be a dotted path."""
        keys = key.split(".")
        temp_data = self.data
        for k in keys[:-1]:
            if k not in temp_data:
                temp_data[k] = {}
            temp_data = temp_data[k]
        temp_data[keys[-1]] = value
        logging.info(f"Set value: {key}={value}")

    def __getitem__(self, key: str, default: typing.Any = None) -> typing.Any:
        """Retrieve a value from the config by key, return default if key is not found."""
        keys = key.split(".")
        temp_data = self.data
        for k in keys:
            if k in temp_data:
                temp_data = temp_data[k]
            else:
                return default
        return temp_data

    @classmethod
    def get_instance(cls, file_path: str = ""):
        """Class method to get the singleton instance with a default config path."""
        if cls._instance is None:
            cls(file_path)
        return cls._instance

    def save(self) -> None:
        """Save the current config data back to the file."""
        rtoml.dump(self.data, self.file_path)


atexit.register(ConfigManager.get_instance().save)
