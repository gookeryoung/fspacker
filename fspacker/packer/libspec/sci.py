import logging

from fspacker.common import PackTarget
from fspacker.packer.libspec.base import ChildLibSpecPacker


class MatplotlibSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        matplotlib={
            "matplotlib",
            "matplotlib.libs",
            "mpl_toolkits",
            "matplotlib-3.7.5-py3.8-nspkg.pth",
            "pylab.py",
        },
        contourpy=set(),
        cycler=set(),
        importlib_resources=set(),
        numpy=set(),
        packaging=set(),
        pillow=set(),
        pyparsing=set(),
        python_dateutil={
            "dateutil",
        },
        zipp=set(),
    )

    def pack(self, lib: str, target: PackTarget):
        logging.info("Using [matplotlib] pack spec")
        super().pack(lib, target)


class PillowSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        pillow={"PIL"},
    )


class NumbaSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        numba=set(),
        cffi={"cffi", "_cffi_backend.cp38-win_amd64"},
        importlib_metadata=set(),
        llvmlite=set(),
        pycparser=set(),
    )
