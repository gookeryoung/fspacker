import os
import pathlib
import platform
import typing

__cache_env = os.getenv("FSPACKER_CACHE")
__libs_env = os.getenv("FSPACKER_LIBS")

PYTHON_VER = platform.python_version()
PYTHON_VER_SHORT = ".".join(PYTHON_VER.split(".")[:2])
MACHINE = platform.machine().lower()

if __cache_env:
    CACHE_DIR = pathlib.Path(__cache_env)
else:
    CACHE_DIR = pathlib.Path("~").expanduser() / ".cache" / "fspacker"

if not CACHE_DIR.is_dir():
    CACHE_DIR.mkdir(parents=True)

if __libs_env:
    LIBS_REPO_DIR = pathlib.Path(__libs_env)
else:
    LIBS_REPO_DIR = CACHE_DIR / "libs-repo"

if not LIBS_REPO_DIR.is_dir():
    LIBS_REPO_DIR.mkdir(parents=True)

CONFIG_FILEPATH = CACHE_DIR / "config.json"
ASSETS_DIR = pathlib.Path(__file__).parent / "assets"
EMBED_REPO_DIR = CACHE_DIR / "embed-repo"
EMBED_FILE_NAME = f"python-{PYTHON_VER}-embed-{MACHINE}.zip"
EMBED_FILEPATH = EMBED_REPO_DIR / EMBED_FILE_NAME
TKINTER_LIB_FILEPATH = ASSETS_DIR / "tkinter-lib.zip"
TKINTER_FILEPATH = ASSETS_DIR / "tkinter.zip"

if not EMBED_REPO_DIR.exists():
    EMBED_REPO_DIR.mkdir(parents=True)

# python mirrors
EMBED_URL_PREFIX: typing.Dict[str, str] = dict(
    official="https://www.python.org/ftp/python/",
    huawei="https://mirrors.huaweicloud.com/python/",
)

# pip mirrors
PIP_URL_PREFIX: typing.Dict[str, str] = dict(
    aliyun="https://mirrors.aliyun.com/pypi/simple/",
    tsinghua="https://pypi.tuna.tsinghua.edu.cn/simple/",
    douban="http://pypi.douban.com/simple/",
    ustc="https://pypi.mirrors.ustc.edu.cn/simple/",
    huawei="https://mirrors.huaweicloud.com/repository/pypi/simple/",
)

# resource files and folders
RES_ENTRIES = (
    "assets",
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
