import pytest

from fspacker.process import Processor
from tests.utils import exec_dist_dir, DIR_EXAMPLES


class TestProcess:
    @pytest.mark.benchmark(group="console")
    def test_pack_ex01(self):
        root_dir = DIR_EXAMPLES / "ex01_helloworld_console"
        proc = Processor(root_dir)
        proc.run()

        assert exec_dist_dir(root_dir / "dist")

    @pytest.mark.benchmark(group="gui")
    def test_pack_ex02(self):
        root_dir = DIR_EXAMPLES / "ex02_hello_gui"
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


# def test_pack_ex13():
#     root_dir = DIR_EXAMPLES / "ex13_pypdf"
#     proc = Processor(root_dir)
#     proc.run()

#     assert exec_dist_dir(root_dir / "dist")


# def test_pack_ex20():
#     root_dir = DIR_EXAMPLES / "ex20_pygame_snake"
#     proc = Processor(root_dir)
#     proc.run()

#     assert exec_dist_dir(root_dir / "dist")


# def test_pack_ex22():
#     root_dir = DIR_EXAMPLES / "ex22_matplotlib"
#     proc = Processor(root_dir)
#     proc.run()

#     assert exec_dist_dir(root_dir / "dist")


# def test_pack_ex23():
#     root_dir = DIR_EXAMPLES / "ex23_numba"
#     proc = Processor(root_dir)
#     proc.run()

#     assert exec_dist_dir(root_dir / "dist")


# def test_pack_ex24():
#     root_dir = DIR_EXAMPLES / "ex24_pandas"
#     proc = Processor(root_dir)
#     proc.run()

#     assert exec_dist_dir(root_dir / "dist")


# def test_pack_ex25():
#     root_dir = DIR_EXAMPLES / "ex25_pytorch"
#     proc = Processor(root_dir)
#     proc.run()

#     assert exec_dist_dir(root_dir / "dist")


# if __name__ == "__main__":
#     pytest.main()
