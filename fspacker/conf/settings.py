import atexit
import os
import pathlib
import platform
import typing
import rtoml

__all__ = [
    "settings",
]


_libs_dir: typing.Optional[pathlib.Path] = None
_cache_dir: typing.Optional[pathlib.Path] = None
_config: typing.Dict[str, typing.Any] = {}


def _get_cache_dir() -> pathlib.Path:
    """Cache directory for fspacker, use user document if not exist."""

    global _cache_dir

    if _cache_dir is None:
        cache_env = os.getenv("FSPACKER_CACHE")
        if cache_env is not None and (cache_path := pathlib.Path(cache_env)).exists():
            _cache_dir = cache_path
        else:
            _cache_dir = pathlib.Path("~").expanduser() / ".cache" / "fspacker"

    return _cache_dir


def _get_libs_dir() -> pathlib.Path:
    """Libs directory for fspacker, use user document if not exist."""

    global _libs_dir

    if _libs_dir is None:
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

    # python
    PYTHON_VER = platform.python_version()
    PYTHON_VER_SHORT = ".".join(PYTHON_VER.split(".")[:2])
    MACHINE = platform.machine().lower()

    # global
    CONFIG = _get_config()
    CACHE_DIR = _get_cache_dir()
    ASSETS_DIR = pathlib.Path(__file__).parent.parent / "assets"
    # resource files and folders
    RES_ENTRIES = (
        "assets",
        "data",
        ".qrc",
    )
    # ignore symbols for folders
    IGNORE_SYMBOLS = (
        "dist-info",
        "__pycache__",
        "site-packages",
        "runtime",
        "dist",
    )
    # gui libs
    GUI_LIBS = (
        "pyside2",
        "pyqt5",
        "pygame",
        "matplotlib",
        "tkinter",
    )
    # mapping between import name and real file name
    LIBNAME_MAPPER = dict(
        pil="Pillow",
        docx="python-docx",
        win32com="pywin32",
        yaml="pyyaml",
        zstd="zstandard",
    )

    # embed
    EMBED_REPO_DIR = CACHE_DIR / "embed-repo"
    EMBED_FILE_NAME = f"python-{PYTHON_VER}-embed-{MACHINE}.zip"
    EMBED_FILE_PATH = EMBED_REPO_DIR / EMBED_FILE_NAME

    # libs
    LIBS_REPO_DIR = _get_libs_dir()
    TKINTER_LIBS = ("tkinter", "matplotlib")

    # tkinter
    TKINTER_LIB_PATH = ASSETS_DIR / "tkinter-lib.zip"
    TKINTER_PATH = ASSETS_DIR / "tkinter.zip"

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Settings()

            # make directories
            cache_dir = _get_cache_dir()
            dirs = (cache_dir, cls.EMBED_REPO_DIR, cls.LIBS_REPO_DIR)
            for directory in dirs:
                if not directory.exists():
                    directory.mkdir(parents=True)

        return cls._instance

    @classmethod
    def save_config(cls):
        _save_config()


settings = Settings.get_instance()
atexit.register(settings.save_config)
