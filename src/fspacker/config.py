import typing

# python 镜像
EMBED_URL_PREFIX: typing.Dict[str, str] = dict(
    official="https://www.python.org/ftp/python/",
    huawei="https://mirrors.huaweicloud.com/python/",
)

# 打包对象资源及库判定规则
RES_DIRS = ("assets",)  # 共用资源
DEP_FILES = ("*.qrc", "*_rc.py")  # 支持打包qrc等文件
IGNORE_DIRS = (
    *RES_DIRS,
    "dist",
    "runtime",
    "site-packages",
    "__pycache__",
    ".ruff_cache",
)
IGNORE_SYMBOLS = (
    "dist-info",
    "__pycache__",
)
GUI_LIBS = ("pyside2", "pyqt5", "pygame", "matplotlib", "tkinter")

# 最多显示文件数
MAX_SHOWN_FILES = 3
