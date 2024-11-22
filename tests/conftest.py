import os
import pathlib
import shutil


def pytest_sessionstart(session):
    for item in session.items:
        if not item.get_closest_marker("no_cache"):
            os.environ["FSPACKER_CACHE"] = str(pathlib.Path.home() / "test-cache")
            os.environ["FSPACKER_LIBS"] = str(pathlib.Path.home() / "test-libs")


def pytest_sessionfinish(session, exitstatus):
    from fspacker.config import CACHE_DIR
    from tests.utils import DIR_EXAMPLES

    if CACHE_DIR.exists():
        shutil.rmtree(CACHE_DIR)

    os.environ.pop("FSPACKER_CACHE", None)

    dist_dirs = (_ for _ in DIR_EXAMPLES.rglob("dist"))
    for dist_dir in dist_dirs:
        shutil.rmtree(dist_dir)

    print("\nClear environment")
