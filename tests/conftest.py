import os
import pathlib
import shutil

import pytest

CWD = pathlib.Path(__file__).parent
DIR_EXAMPLES = CWD.parent / "examples"
TEST_CACHE_DIR = pathlib.Path.home() / "test-cache"
TEST_LIB_DIR = pathlib.Path.home() / "test-libs"


def pytest_sessionstart(session):
    """Start before pytest session"""
    print(f"\nStart environment, {session=}")
    os.environ["FSPACKER_CACHE"] = str(TEST_CACHE_DIR)
    os.environ["FSPACKER_LIBS"] = str(TEST_LIB_DIR)


def pytest_sessionfinish(session, exitstatus):
    print(f"\nClear environment, {session=}, {exitstatus=}")


@pytest.fixture
def clear_cache():
    for dir_ in (TEST_CACHE_DIR, TEST_LIB_DIR):
        if dir_.exists():
            shutil.rmtree(dir_)

    print(f"\nClear cache and libs")


@pytest.fixture
def base_examples():
    return list(DIR_EXAMPLES / x for x in ("base_helloworld",))


@pytest.fixture
def gui_examples():
    return list(
        DIR_EXAMPLES / x
        for x in (
            "gui_tkinter",
            "gui_pyside2",
        )
    )


@pytest.fixture
def math_examples():
    return list(DIR_EXAMPLES / x for x in ("math_matplotlib",))
