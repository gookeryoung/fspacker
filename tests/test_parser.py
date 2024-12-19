from fspacker.parser.source import SourceParser
from tests.utils import DIR_EXAMPLES


class TestSourceParser:
    def test_source_parser(self):
        parser = SourceParser(root_dir=DIR_EXAMPLES / "base_helloworld")
        parser.parse(DIR_EXAMPLES / "base_helloworld" / "base_helloworld.py")
        assert "base_helloworld" in parser.targets.keys()

        target = parser.targets["base_helloworld"]
        assert target.libs == {"lxml"}
        assert target.sources == {"modules", "module_c", "module_d", "core"}

    def test_gui_tkinter(self):
        root_dir = DIR_EXAMPLES / "gui_tkinter"
        parser = SourceParser(root_dir=root_dir)
        parser.parse(root_dir / "gui_tkinter.py")
        assert "gui_tkinter" in parser.targets.keys()

        target = parser.targets["gui_tkinter"]
        assert target.libs == {"yaml"}
        assert target.sources == {"modules", "config", "assets"}
        assert target.extra == {"tkinter"}

    def test_gui_pyside2(self):
        parser = SourceParser(root_dir=DIR_EXAMPLES / "gui_pyside2")
        parser.parse(DIR_EXAMPLES / "gui_pyside2" / "gui_pyside2.py")
        assert "gui_pyside2" in parser.targets.keys()

        target = parser.targets["gui_pyside2"]
        assert target.libs == {"pyside2"}
        assert target.sources == {"depends", "assets", "resources_rc"}
