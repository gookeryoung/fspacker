from fspacker.packer.libspec.base import ChildLibSpecPacker


class MatplotlibSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        matplotlib={
            "matplotlib/",
            "matplotlib.libs/",
            "mpl_toolkits/",
            "pylab.py",
        },
    )
    EXCLUDES = dict(
        matplotlib={"matplotlib-.*.pth"},
    )


class NumbaSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        numba={"numba/", "data/"},
        cffi=set(),
        pycparser=set(),
    )


class TorchSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        torch={"functorch/", "torch/", "torchgen/"},
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
