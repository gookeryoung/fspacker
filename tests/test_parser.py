from fspacker.parser.source import SourceParser


class TestSourceParser:
    def test_source_parser(self, dir_examples):
        parser = SourceParser(root_dir=dir_examples / "base_helloworld")
        parser.parse(dir_examples / "base_helloworld" / "base_helloworld.py")
        assert "base_helloworld" in parser.targets.keys()

        target = parser.targets["base_helloworld"]
        assert target.libs == {"lxml"}
        assert target.sources == {"modules", "module_c", "module_d", "core"}

    def test_gui_tkinter(self, dir_examples):
        root_dir = dir_examples / "gui_tkinter"
        parser = SourceParser(root_dir=root_dir)
        parser.parse(root_dir / "gui_tkinter.py")
        assert "gui_tkinter" in parser.targets.keys()

        target = parser.targets["gui_tkinter"]
        assert target.libs == {"yaml"}
        assert target.sources == {"modules", "config", "assets"}
        assert target.extra == {"tkinter"}

    def test_gui_pyside2(self, dir_examples):
        parser = SourceParser(root_dir=dir_examples / "gui_pyside2")
        parser.parse(dir_examples / "gui_pyside2" / "gui_pyside2.py")
        assert "gui_pyside2" in parser.targets.keys()

        target = parser.targets["gui_pyside2"]
        assert target.libs == {"pyside2"}
        assert target.sources == {"depends", "assets", "resources_rc"}

    def test_math_numba(self, dir_examples):
        parser = SourceParser(root_dir=dir_examples / "math_numba")
        parser.parse(dir_examples / "math_numba" / "math_numba.py")
        assert "math_numba" in parser.targets.keys()

        target = parser.targets["math_numba"]
        assert target.libs == {"numba", "numpy"}
        assert target.sources == set()
