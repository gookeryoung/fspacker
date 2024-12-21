from fspacker.packer.libspec.base import ChildLibSpecPacker


class MatplotlibSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        matplotlib={
            "matplotlib/*",
            "matplotlib.libs/*",
            "mpl_toolkits/*",
            "pylab.py",
        },
        six=set(),
    )
    EXCLUDES = dict(
        matplotlib={"matplotlib-.*.pth"},
    )


class NumbaSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        numba={
            "numba/*",
            "data/*",
        },
        importlib_metadata=set(),
        cffi=set(),
        pycparser=set(),
        zipp=set(),
    )


class PandasSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        pandas=set(),
        six=set(),
    )


class TorchSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        torch={"functorch/*", "torch/*", "torchgen/*"},
        urllib3=set(),
        chardet=set(),
        certifi=set(),
        idna=set(),
    )
    EXCLUDES = dict(
        torch={
            # for debug
            "torch/utils/bottleneck/*",
            "torch/utils/checkpoint/*",
            "torch/utils/tensorboard/*",
            # for test
            "torch/utils/data/dataset/*",
            "torch/utils/data/dataloader/*",
        }
    )
