import typing

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
