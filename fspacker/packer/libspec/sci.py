import logging

from fspacker.common import PackTarget
from fspacker.packer.libspec.base import ChildLibSpecPacker


class MatplotlibSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        matplotlib={"matplotlib/", "matplotlib.libs/", "mpl_toolkits/", "pylab.py"},
        contourpy=set(),
        cycler=set(),
        importlib_resources=set(),
        numpy=set(),
        kiwisolver=set(),
        packaging=set(),
        pillow=set(),
        pyparsing=set(),
        python_dateutil={"^dateutil"},
        zipp=set(),
    )

    def pack(self, lib: str, target: PackTarget):
        logging.info("Using [matplotlib] pack spec")
        super().pack(lib, target)


class PillowSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        pillow={
            "PIL/",
        },
    )


class NumbaSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        numba=set(),
        cffi={"cffi", "_cffi_backend.cp38-win_amd64"},
        importlib_metadata=set(),
        llvmlite=set(),
        pycparser=set(),
    )


class SymPyPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        sympy=set(),
        mpmath=set(),
    )


class TorchSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        torch={"functorch/", "torch/", "torchgen/"},
        fsspec=set(),
        filelock=set(),
        jinja2=set(),
        MarkupSafe=set(),
        matplotlib=set(),
        sympy=set(),
        typing_extensions=set(),
    )
    EXCLUDES = dict(
        torch={
            # for debug
            "torch/utils/bottleneck/",
            "torch/utils/checkpoint/",
            "torch/utils/tensorboard/",
            # for test
            "torch/utils/data/dataset/",
            "torch/utils/data/dataloader/",
        }
    )


class TorchVisionSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        torchvision={
            "torchvision/",
        },
        torch=set(),
        numpy=set(),
        pillow=set(),
    )
