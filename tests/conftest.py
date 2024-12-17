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
def ex02():
    return DIR_EXAMPLES / "ex02_tkinter"
