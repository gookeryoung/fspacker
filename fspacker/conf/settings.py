import atexit
import os
import pathlib
import platform
import typing

import rtoml

__all__ = [
    "settings",
]


_config: typing.Dict[str, typing.Any] = {}


def _get_cache_dir() -> pathlib.Path:
    """Cache directory for fspacker, use user document if not exist."""

    cache_env = os.getenv("FSPACKER_CACHE")
    if cache_env is not None:
        _cache_dir = pathlib.Path(cache_env)
    else:
        _cache_dir = pathlib.Path("~").expanduser() / ".cache" / "fspacker"

    return _cache_dir


def _get_libs_dir() -> pathlib.Path:
    """Libs directory for fspacker, use user document if not exist."""
    cache_env = os.getenv("FSPACKER_LIBS")
    if cache_env is not None and (cache_path := pathlib.Path(cache_env)).exists():
        _libs_dir = cache_path
    else:
        _libs_dir = _get_cache_dir() / "libs-repo"

    return _libs_dir


def _get_config() -> typing.Dict[str, typing.Any]:
    """Read config from `config.toml`."""

    global _config

    if not len(_config):
        config_file = _get_cache_dir() / "config.toml"
        if config_file.exists():
            _config = rtoml.load(config_file)

    return _config


def _save_config() -> None:
    """Save config file while exiting."""
    global _config

    if len(_config):
        config_file = _get_cache_dir() / "config.toml"
        rtoml.dump(_config, config_file, pretty=True, none_value=None)


class Settings:
    """Global settings for fspacker."""

    # global
    src_dir = pathlib.Path(__file__).parent.parent
    assets_dir = src_dir / "assets"
    # resource files and folders
    res_entries = (
        "assets",
        "data",
        ".qrc",
    )
    # ignore symbols for folders
    ignore_symbols = (
        "dist-info",
        "__pycache__",
        "site-packages",
        "runtime",
        "dist",
    )
    # gui libs
    gui_libs = (
        "pyside2",
        "pyqt5",
        "pygame",
        "matplotlib",
        "tkinter",
    )
    # mapping between import name and real file name
    libname_mapper = dict(
        pil="Pillow",
        docx="python-docx",
        win32com="pywin32",
        yaml="pyyaml",
        zstd="zstandard",
    )

    # libs
    tkinter_libs = ("tkinter", "matplotlib")

    # tkinter
    tkinter_lib_path = assets_dir / "tkinter-lib.zip"
    tkinter_path = assets_dir / "tkinter.zip"

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Settings()

            # make directories
            dirs = (
                cls._instance.cache_dir,
                cls._instance.embed_dir,
                cls._instance.libs_dir,
            )
            for directory in dirs:
                if not directory.exists():
                    directory.mkdir(parents=True)

        return cls._instance

    @property
    def python_ver(self):
        return platform.python_version()

    @property
    def python_ver_short(self):
        return ".".join(self.python_ver.split(".")[:2])

    @property
    def machine(self):
        return platform.machine().lower()

    @property
    def cache_dir(self):
        return _get_cache_dir()

    @property
    def libs_dir(self):
        return _get_libs_dir()

    @property
    def embed_dir(self):
        return _get_cache_dir() / "embed-repo"

    @property
    def embed_filename(self):
        return f"python-{self.python_ver}-embed-{self.machine}.zip"

    @property
    def embed_filepath(self):
        return self.embed_dir / self.embed_filename

    @property
    def config(self):
        return _get_config()

    @classmethod
    def save_config(cls):
        _save_config()


settings = Settings.get_instance()
atexit.register(settings.save_config)
