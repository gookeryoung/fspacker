import logging

from fspacker.common import BuildTarget


class BasePacker:
    def pack(self, target: BuildTarget):
        for dir_ in (target.dist_dir, target.runtime_dir, target.packages_dir):
            if not dir_.exists():
                logging.info(f"创建目录: [{dir_}]")
                dir_.mkdir(parents=True)
