import logging
import shutil

from fspacker.common import BuildTarget
from fspacker.config import TKINTER_LIB_FILEPATH, TKINTER_FILEPATH
from fspacker.packer.libspec.base import BaseLibrarySpecPacker


class TkinterPacker(BaseLibrarySpecPacker):
    def pack(self, target: BuildTarget):
        if "tkinter" in target.extra:
            logging.info("打包tkinter依赖文件")
            shutil.unpack_archive(TKINTER_LIB_FILEPATH, target.dist_dir, "zip")
            shutil.unpack_archive(TKINTER_FILEPATH, target.packages_dir, "zip")
