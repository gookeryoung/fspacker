import gc

import pytest

from fspacker.process import Processor
from tests.common import DIR_EXAMPLES, exec_dist_dir


@pytest.fixture(autouse=True)
def disable_gc():
    gc.disable()
    yield
    gc.enable()


@pytest.mark.benchmark(group="console")
def test_pack_ex01(disable_gc):
    root_dir = DIR_EXAMPLES / "ex01_helloworld_console"
    proc = Processor(root_dir)
    proc.run()

    assert exec_dist_dir(root_dir / "dist")


@pytest.mark.benchmark(group="tkinter")
def test_pack_ex02(disable_gc):
    root_dir = DIR_EXAMPLES / "ex02_hello_gui"
    proc = Processor(root_dir)
    proc.run()

    assert exec_dist_dir(root_dir / "dist")


@pytest.mark.benchmark(group="pyside2")
def test_pack_ex03(disable_gc):
    root_dir = DIR_EXAMPLES / "ex03_pyside2_simple"
    proc = Processor(root_dir)
    proc.run()

    assert exec_dist_dir(root_dir / "dist")


@pytest.mark.benchmark(group="pyside2")
def test_pack_ex04(disable_gc):
    root_dir = DIR_EXAMPLES / "ex04_pyside_complex"
    proc = Processor(root_dir)
    proc.run()

    assert exec_dist_dir(root_dir / "dist")


def test_pack_ex05(disable_gc):
    root_dir = DIR_EXAMPLES / "ex05_tkinter"
    proc = Processor(root_dir)
    proc.run()

    assert exec_dist_dir(root_dir / "dist")


def test_pack_ex12(disable_gc):
    root_dir = DIR_EXAMPLES / "ex12_web_bottle"
    proc = Processor(root_dir)
    proc.run()

    assert exec_dist_dir(root_dir / "dist")


def test_pack_ex13(disable_gc):
    root_dir = DIR_EXAMPLES / "ex13_pypdf"
    proc = Processor(root_dir)
    proc.run()

    assert exec_dist_dir(root_dir / "dist")


def test_pack_ex20(disable_gc):
    root_dir = DIR_EXAMPLES / "ex20_pygame_snake"
    proc = Processor(root_dir)
    proc.run()

    assert exec_dist_dir(root_dir / "dist")


def test_pack_ex22(disable_gc):
    root_dir = DIR_EXAMPLES / "ex22_matplotlib"
    proc = Processor(root_dir)
    proc.run()

    assert exec_dist_dir(root_dir / "dist")


def test_pack_ex23(disable_gc):
    root_dir = DIR_EXAMPLES / "ex23_numba"
    proc = Processor(root_dir)
    proc.run()

    assert exec_dist_dir(root_dir / "dist")


def test_pack_ex24(disable_gc):
    root_dir = DIR_EXAMPLES / "ex24_pandas"
    proc = Processor(root_dir)
    proc.run()

    assert exec_dist_dir(root_dir / "dist")


if __name__ == "__main__":
    pytest.main()
