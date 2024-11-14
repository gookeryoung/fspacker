import pytest

from fspacker.core.process import Processor
from fspacker.tests.common import DIR_EXAMPLES, exec_dist_dir


class TestProcess:
    def test_pack_ex01(self):
        root_dir = DIR_EXAMPLES / "ex01_helloworld_console"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    def test_pack_ex12(self):
        root_dir = DIR_EXAMPLES / "ex12_web_bottle"
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


if __name__ == "__main__":
    pytest.main()
