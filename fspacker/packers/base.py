import logging
import typing

from fspacker.core.target import PackTarget


class BasePacker:
    SPECS: typing.Dict[str, typing.Any] = {}

    def pack(self, target: PackTarget):
        dirs = list(
            _
            for _ in (target.dist_dir, target.runtime_dir, target.packages_dir)
            if not _.exists()
        )

        if len(dirs):
            logging.info(
                f"Create folder{'' if len(dirs) == 1 else 's'}: {list(_.name for _ in dirs)}"
            )
            for dir_ in dirs:
                dir_.mkdir(parents=True)
