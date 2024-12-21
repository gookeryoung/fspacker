import os
import pathlib
import shutil
import subprocess
import time
import typing

import psutil
import pytest

from fspacker.config import TEST_CALL_TIMEOUT
from fspacker.process import Processor

CWD = pathlib.Path(__file__).parent
DIR_EXAMPLES = CWD.parent / "examples"
TEST_CACHE_DIR = pathlib.Path.home() / "test-cache"
TEST_LIB_DIR = pathlib.Path.home() / "test-libs"


def _call_app(app: str, timeout=TEST_CALL_TIMEOUT):
    """Call application and try running it in [timeout] seconds."""

    try:
        proc = subprocess.Popen(
            [app], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        time.sleep(1)
        for _ in range(timeout):
            if proc.poll() is not None:
                if proc.returncode == 0:
                    print(f"App [{app}] type: [Console],  run successfully.")
                    proc.terminate()
                    return True
                else:
                    print(
                        f"App [{app}]exited prematurely with return code [{proc.returncode}]."
                    )
                    return False

            if not any(proc.pid == p.pid for p in psutil.process_iter(["pid"])):
                print(
                    f"Process [{proc.pid}] not found among running processes."
                )
                return False

            time.sleep(1)
        print(f"App [{app}] type: [GUI],  run successfully.")
        proc.terminate()
        return True
    except Exception as e:
        print(f"An error occurred while trying to launch the application: {e}.")
        return False


def pytest_sessionstart(session):
    """Called before each pytest session."""

    print(f"\nStart environment, {session=}")
    os.environ["FSPACKER_CACHE"] = str(TEST_CACHE_DIR)
    os.environ["FSPACKER_LIBS"] = str(TEST_LIB_DIR)

    # Clear all dist files before test
    dist_folders = list(x for x in DIR_EXAMPLES.rglob("dist") if x.is_dir())
    for dist_folder in dist_folders:
        shutil.rmtree(dist_folder)


def pytest_sessionfinish(session, exitstatus):
    """Called after each pytest session."""

    print(f"\nClear environment, {session=}, {exitstatus=}")


@pytest.fixture
def run_proc():
    """Run processor to build example code and test if it can execute."""

    def runner(args: typing.List[pathlib.Path]):
        for arg in args:
            if isinstance(arg, pathlib.Path):
                proc = Processor(arg)
                proc.run()

                dist_dir = arg / "dist"
                os.chdir(dist_dir)
                exe_files = list(_ for _ in dist_dir.glob("*.exe"))

                if not len(exe_files):
                    print(f"[#] No exe file found for [{arg.name}]")
                    return False

                print(f"\n[#] Running executable: [{exe_files[0].name}]")
                call_result = _call_app(exe_files[0].as_posix())
                if not call_result:
                    print(f"[#] Running failed: [{exe_files[0].name}]")
                    return False
        return True

    return runner


@pytest.fixture
def dir_examples():
    return DIR_EXAMPLES


@pytest.fixture
def base_examples():
    return list(
        DIR_EXAMPLES / x
        for x in (
            "base_helloworld",
            "base_office",
        )
    )


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
def game_examples():
    return list(DIR_EXAMPLES / x for x in ("game_pygame",))


@pytest.fixture
def math_examples():
    return list(
        DIR_EXAMPLES / x
        for x in (
            "math_numba",
            "math_pandas",
            "math_torch",
            "math_matplotlib",
        )
    )
