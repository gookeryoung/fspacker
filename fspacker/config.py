import os
import pathlib
import platform
import typing

__cache_env = os.getenv("FSPACKER_CACHE")

PYTHON_VER = platform.python_version()
PYTHON_VER_SHORT = ".".join(PYTHON_VER.split(".")[:2])
MACHINE = platform.machine().lower()

if __cache_env:
    CACHE_DIR = pathlib.Path(__cache_env)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
else:
    CACHE_DIR = pathlib.Path("~").expanduser() / ".cache" / "fspacker"

LIBS_REPO_DIR = CACHE_DIR / "libs-repo"
CONFIG_FILEPATH = CACHE_DIR / "config.json"
ASSETS_DIR = pathlib.Path(__file__).parent / "assets"
EMBED_REPO_DIR = CACHE_DIR / "embed-repo"
EMBED_FILE_NAME = f"python-{PYTHON_VER}-embed-{MACHINE}.zip"
EMBED_FILEPATH = EMBED_REPO_DIR / EMBED_FILE_NAME
TKINTER_LIB_FILEPATH = ASSETS_DIR / "tkinter-lib.zip"
TKINTER_FILEPATH = ASSETS_DIR / "tkinter.zip"

# python mirrors
EMBED_URL_PREFIX: typing.Dict[str, str] = dict(
    official="https://www.python.org/ftp/python/",
    huawei="https://mirrors.huaweicloud.com/python/",
)

# ignore symbols for folders
IGNORE_SYMBOLS = (
    "dist-info",
    "__pycache__",
    "site-packages",
    "runtime",
    "dist",
)
GUI_LIBS = (
    "pyside2",
    "pyqt5",
    "pygame",
    "matplotlib",
    "tkinter",
)

TKINTER_LIBS = (
    "tkinter",
    "matplotlib",
)

# 最多显示文件数
MAX_SHOWN_FILES = 3
TEST_CALL_TIMEOUT = 0.05
