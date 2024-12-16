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

    def test_pack_ex02(self):
        root_dir = DIR_EXAMPLES / "ex02_tkinter"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex02_single_file(self):
        root_dir = DIR_EXAMPLES / "ex02_tkinter"
        proc = Processor(root_dir, root_dir / "ex02_tkinter.py")
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex07(self):
        root_dir = DIR_EXAMPLES / "ex07_tarfile"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")
