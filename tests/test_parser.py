import typing

import pytest

from fspacker.core.parsers import parsers


@pytest.fixture
def run_parser(dir_examples):
    """Run source parser"""

    def runner(
        arg: str,
        libs: typing.Optional[typing.Set[str]] = None,
        sources: typing.Optional[typing.Set[str]] = None,
        extra: typing.Optional[typing.Set[str]] = None,
    ) -> None:
        parsers.parse(dir_examples / arg / f"{arg}.py", dir_examples / arg)
        assert arg in parsers.TARGETS.keys()

        libs = set() if libs is None else libs
        sources = set() if sources is None else sources
        extra = set() if extra is None else extra

        target = parsers.TARGETS.get(arg)
        assert target.libs == libs
        assert target.sources == sources
        assert target.extra == extra

    return runner


def test_source_parser(run_parser):
    run_parser(
        "base_helloworld",
        {"defusedxml", "orderedset"},
        {
            "modules",
            "module_c",
            "module_d",
            "core",
            "mathtools",
        },
    )


def test_gui_tkinter(run_parser):
    run_parser(
        "gui_tkinter",
        {"yaml"},
        {"modules", "config", "assets"},
        {"tkinter"},
    )


def test_gui_pyside2(run_parser):
    run_parser("gui_pyside2", {"pyside2"}, {"depends", "assets", "resources_rc"})


def test_math_matplotlib(run_parser):
    run_parser("math_matplotlib", {"numpy", "matplotlib"}, set(), {"tkinter"})


def test_math_numba(run_parser):
    run_parser("math_numba", {"numba", "numpy"})


def test_math_pandas(run_parser):
    run_parser("math_pandas", {"numpy", "matplotlib", "pandas"}, set(), {"tkinter"})


def test_math_torch(run_parser):
    run_parser(
        "math_torch",
        {"torch", "torchvision"},
        set(),
        set(),
    )


def test_web_bottle(run_parser):
    run_parser("web_bottle", {"bottle"})
