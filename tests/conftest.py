import os
import pathlib
import shutil

from tests.utils import DIR_EXAMPLES


def pytest_sessionstart(session):
    os.environ["FSPACKER_CACHE"] = str(pathlib.Path.home() / "test-cache")
    print("Set environment before pytest")


def pytest_sessionfinish(session, exitstatus):
    from fspacker.config import CACHE_DIR

    if CACHE_DIR.exists():
        shutil.rmtree(CACHE_DIR)

    os.environ.pop("FSPACKER_CACHE", None)

    dist_dirs = (_ for _ in DIR_EXAMPLES.rglob("dist"))
    for dist_dir in dist_dirs:
        shutil.rmtree(dist_dir)

    print("\nClear environment")
