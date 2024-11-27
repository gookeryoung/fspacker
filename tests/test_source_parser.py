from fspacker.parser.source import SourceParser
from tests.utils import DIR_EXAMPLES


class TestSourcePacker:
    def test_ex01_source_parser(self):
        parser = SourceParser(
            targets={}, root_dir=DIR_EXAMPLES / "ex01_helloworld_console"
        )
        parser.parse(
            DIR_EXAMPLES / "ex01_helloworld_console" / "ex01_helloworld_console.py"
        )
        assert "ex01_helloworld_console" in parser.targets.keys()

        target = parser.targets["ex01_helloworld_console"]
        assert len(target.ast) == 0
        assert len(target.deps) == 2

    def test_ex02_source_parser(self):
        parser = SourceParser(targets={}, root_dir=DIR_EXAMPLES / "ex02_cross_import")
        parser.parse(DIR_EXAMPLES / "ex02_cross_import" / "ex02_cross_import.py")
        assert "ex02_cross_import" in parser.targets.keys()

        target = parser.targets["ex02_cross_import"]
        assert len(target.ast) == 0
        assert len(target.deps) == 1

    def test_ex03_source_parser(self):
        parser = SourceParser(targets={}, root_dir=DIR_EXAMPLES / "ex03_pyside2_simple")
        parser.parse(DIR_EXAMPLES / "ex03_pyside2_simple" / "ex03_pyside2_simple.py")
        assert "ex03_pyside2_simple" in parser.targets.keys()

        target = parser.targets["ex03_pyside2_simple"]
        assert len(target.ast) == 1
        assert len(target.deps) == 0
