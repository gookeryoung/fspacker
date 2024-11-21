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
    EXCLUDES = dict(
        matplotlib={"matplotlib-.*.pth"},
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
