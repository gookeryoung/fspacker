import pytest

from fspacker.core.process import Processor
from tests.common import DIR_EXAMPLES, exec_dist_dir


class TestProcess:
    def test_pack_ex01(self):
        root_dir = DIR_EXAMPLES / "ex01_helloworld_console"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex02(self):
        root_dir = DIR_EXAMPLES / "ex02_hello_gui"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex03(self):
        root_dir = DIR_EXAMPLES / "ex03_pyside2_simple"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex04(self):
        root_dir = DIR_EXAMPLES / "ex04_pyside_complex"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex05(self):
        root_dir = DIR_EXAMPLES / "ex05_tkinter"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex12(self):
        root_dir = DIR_EXAMPLES / "ex12_web_bottle"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex13(self):
        root_dir = DIR_EXAMPLES / "ex13_pypdf"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex14(self):
        root_dir = DIR_EXAMPLES / "ex14_py7zr"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex20(self):
        root_dir = DIR_EXAMPLES / "ex20_pygame_snake"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex22(self):
        root_dir = DIR_EXAMPLES / "ex22_matplotlib"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex23(self):
        root_dir = DIR_EXAMPLES / "ex23_numba"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex24(self):
        root_dir = DIR_EXAMPLES / "ex24_pandas"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")


if __name__ == "__main__":
    pytest.main()
