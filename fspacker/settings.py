import os
import pathlib
import platform
import typing

__all__ = [
    "settings",
]


_libs_dir: typing.Optional[pathlib.Path] = None
_cache_dir: typing.Optional[pathlib.Path] = None


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

    global _cache_dir

    if _cache_dir is None:
        cache_env = os.getenv("FSPACKER_LIBS")
        if cache_env is not None and (cache_path := pathlib.Path(cache_env)).exists():
            _cache_dir = cache_path
        else:
            _cache_dir = _get_cache_dir() / "libs-repo"

    return _cache_dir


class Settings:
    """Global settings for fspacker."""

    # python
    PYTHON_VER = platform.python_version()
    PYTHON_VER_SHORT = ".".join(PYTHON_VER.split(".")[:2])
    MACHINE = platform.machine().lower()

    # global
    CACHE_DIR = _get_cache_dir()
    ASSETS_DIR = pathlib.Path(__file__).parent / "assets"
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


settings = Settings.get_instance()
