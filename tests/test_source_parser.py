import pytest

from fspacker.common import PackConfig
from fspacker.parser.source import SourceParser
from tests.common import DIR_EXAMPLES


def test_ex01_source_parser():
    parser = SourceParser(
        PackConfig(targets={}),
        root_dir=DIR_EXAMPLES / "ex01_helloworld_console",
    )
    parser.parse(DIR_EXAMPLES / "ex01_helloworld_console" / "ex01_helloworld_console.py")
    assert "ex01_helloworld_console" in parser.config.targets.keys()

    target = parser.config.targets["ex01_helloworld_console"]
    assert len(target.ast) == 0
    assert len(target.deps) == 0


def test_ex02_source_parser():
    parser = SourceParser(
        PackConfig(targets={}),
        root_dir=DIR_EXAMPLES / "ex02_hello_gui",
    )
    parser.parse(DIR_EXAMPLES / "ex02_hello_gui" / "ex02_hello_gui.py")
    assert "ex02_hello_gui" in parser.config.targets.keys()

    target = parser.config.targets["ex02_hello_gui"]
    assert len(target.ast) == 0
    assert len(target.deps) == 0


def test_ex03_source_parser():
    parser = SourceParser(
        PackConfig(targets={}),
        root_dir=DIR_EXAMPLES / "ex03_pyside2_simple",
    )
    parser.parse(DIR_EXAMPLES / "ex03_pyside2_simple" / "ex03_pyside2_simple.py")
    assert "ex03_pyside2_simple" in parser.config.targets.keys()

    target = parser.config.targets["ex03_pyside2_simple"]
    assert len(target.ast) == 1
    assert len(target.deps) == 0


if __name__ == "__main__":
    pytest.main()
