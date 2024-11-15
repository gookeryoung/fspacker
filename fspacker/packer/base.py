import logging

from fspacker.common import PackTarget


class BasePacker:
    def pack(self, target: PackTarget):
        for dir_ in (target.dist_dir, target.runtime_dir, target.packages_dir):
            if not dir_.exists():
                logging.info(f"Create directory: [{dir_}]")
                dir_.mkdir(parents=True)
