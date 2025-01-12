import typing

import pytest

from fspacker.core.parsers import parser_factory


@pytest.fixture
def run_parser(dir_examples):
    """Run source parser"""

    def runner(
        arg: str,
        libs: typing.Optional[typing.Set[str]] = None,
        sources: typing.Optional[typing.Set[str]] = None,
        extra: typing.Optional[typing.Set[str]] = None,
    ) -> None:
        parser_factory.parse(dir_examples / arg / f"{arg}.py", dir_examples / arg)
        assert arg in parser_factory.TARGETS.keys()

        libs = set() if libs is None else libs
        sources = set() if sources is None else sources
        extra = set() if extra is None else extra

        target = parser_factory.TARGETS.get(arg)
        assert target.libs == libs
        assert target.sources == sources
        assert target.extra == extra

    return runner


class TestSourceParser:
    def test_source_parser(self, run_parser):
        run_parser(
            "base_helloworld",
            {"lxml", "orderedset"},
            {
                "modules",
                "module_c",
                "module_d",
                "core",
                "mathtools",
            },
        )

    def test_gui_tkinter(self, run_parser):
        run_parser(
            "gui_tkinter",
            {"yaml"},
            {"modules", "config", "assets"},
            {"tkinter"},
        )

    def test_gui_pyside2(self, run_parser):
        run_parser("gui_pyside2", {"pyside2"}, {"depends", "assets", "resources_rc"})

    def test_math_numba(self, run_parser):
        run_parser("math_numba", {"numba", "numpy"})
