from fspacker.parser.source import SourceParser
from utils import DIR_EXAMPLES


class TestSourceParser:
    def test_ex01(self):
        parser = SourceParser(
            targets={}, root_dir=DIR_EXAMPLES / "ex01_helloworld_console"
        )
        parser.parse(
            DIR_EXAMPLES
            / "ex01_helloworld_console"
            / "ex01_helloworld_console.py"
        )
        assert "ex01_helloworld_console" in parser.targets.keys()

        target = parser.targets["ex01_helloworld_console"]
        assert target.libs == {"lxml"}
        assert target.sources == {"modules", "module_c", "module_d", "core"}

    def test_ex02(self):
        root_dir = DIR_EXAMPLES / "ex02_tkinter"
        parser = SourceParser(targets={}, root_dir=root_dir)
        parser.parse(root_dir / "ex02_tkinter.py")
        assert "ex02_tkinter" in parser.targets.keys()

        target = parser.targets["ex02_tkinter"]
        assert target.libs == {"yaml"}
        assert target.sources == {"modules", "config", "assets"}
        assert target.extra == {"tkinter"}

    def test_ex03(self):
        parser = SourceParser(
            targets={}, root_dir=DIR_EXAMPLES / "ex03_pyside2_simple"
        )
        parser.parse(
            DIR_EXAMPLES / "ex03_pyside2_simple" / "ex03_pyside2_simple.py"
        )
        assert "ex03_pyside2_simple" in parser.targets.keys()

        target = parser.targets["ex03_pyside2_simple"]
        assert target.libs == {"pyside2"}
        assert target.sources == set()
