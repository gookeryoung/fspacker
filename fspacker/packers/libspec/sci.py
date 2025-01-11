from fspacker.packers.libspec.base import ChildLibSpecPacker


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
            "numba*data/*",
        },
        importlib_metadata=set(),
        cffi=set(),
        pycparser=set(),
        zipp=set(),
    )


class NumpySpecPacker(ChildLibSpecPacker):
    EXCLUDES = dict(
        numpy={
            "numpy/_pyinstaller/*",
            "numpy/tests/*",
        }
    )


class PandasSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        pandas=set(),
        six=set(),
    )


class TorchSpecPacker(ChildLibSpecPacker):
    PATTERNS = dict(
        torch=set(),
        certifi=set(),
        chardet=set(),
        idna=set(),
        numpy=set(),
        mpmath=set(),
        urllib3=set(),
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
