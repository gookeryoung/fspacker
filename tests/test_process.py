import pytest

from fspacker.process import Processor
from tests.utils import DIR_EXAMPLES, exec_dist_dir


class TestProcess:
    @pytest.mark.benchmark(group="console")
    def test_pack_ex01(self):
        root_dir = DIR_EXAMPLES / "ex01_helloworld_console"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    @pytest.mark.benchmark(group="console")
    def test_pack_ex02(self):
        root_dir = DIR_EXAMPLES / "ex02_cross_import"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    @pytest.mark.benchmark(group="gui")
    def test_pack_ex03(self):
        root_dir = DIR_EXAMPLES / "ex03_pyside2_simple"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    @pytest.mark.benchmark(group="gui")
    def test_pack_ex04(self):
        root_dir = DIR_EXAMPLES / "ex04_pyside_complex"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    @pytest.mark.benchmark(group="gui")
    def test_pack_ex05(self):
        root_dir = DIR_EXAMPLES / "ex05_tkinter"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    @pytest.mark.benchmark(group="web")
    def test_pack_ex12(self):
        root_dir = DIR_EXAMPLES / "ex12_web_bottle"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    @pytest.mark.benchmark(group="office")
    def test_pack_ex13(self):
        root_dir = DIR_EXAMPLES / "ex13_pypdf"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    @pytest.mark.benchmark(group="game")
    def test_pack_ex20(self):
        root_dir = DIR_EXAMPLES / "ex20_pygame_snake"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    @pytest.mark.benchmark(group="sci")
    def test_pack_ex22(self):
        root_dir = DIR_EXAMPLES / "ex22_matplotlib"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    @pytest.mark.no_cache
    def test_pack_ex22_no_cache(self):
        root_dir = DIR_EXAMPLES / "ex22_matplotlib"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")
