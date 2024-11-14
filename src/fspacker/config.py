import os
import pathlib
import platform
import typing

__libs_env = os.getenv("FSPACKER_LIB_DIR")

PYTHON_VER = platform.python_version()
PYTHON_VER_SHORT = ".".join(PYTHON_VER.split(".")[:2])
MACHINE = platform.machine().lower()
CACHE_DIR = pathlib.Path("~").expanduser() / ".cache" / "fspacker"
CONFIG_FILEPATH = CACHE_DIR / "config.json"
ASSETS_DIR = pathlib.Path(__file__).parent / "assets"
EMBED_REPO_DIR = CACHE_DIR / "embed-repo"
EMBED_FILE_NAME = f"python-{PYTHON_VER}-embed-{MACHINE}.zip"
EMBED_FILEPATH = EMBED_REPO_DIR / EMBED_FILE_NAME
DEPENDS_FILEPATH = ASSETS_DIR / "depend_tree.toml"
TKINTER_LIB_FILEPATH = ASSETS_DIR / "tkinter-lib.zip"
TKINTER_FILEPATH = ASSETS_DIR / "tkinter.zip"

if __libs_env and pathlib.Path(__libs_env).expanduser().exists():
    pathlib.Path(__libs_env).expanduser()
else:
    LIBS_REPO_DIR = CACHE_DIR / "libs-repo"

# python 镜像
EMBED_URL_PREFIX: typing.Dict[str, str] = dict(
    official="https://www.python.org/ftp/python/",
    huawei="https://mirrors.huaweicloud.com/python/",
)

# 打包对象资源及库判定规则
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

# 最多显示文件数
MAX_SHOWN_FILES = 3
