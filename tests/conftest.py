import os
import pathlib
import shutil
import subprocess
import time
import typing

import psutil
import pytest

from fspacker.process import Processor

CWD = pathlib.Path(__file__).parent
DIR_EXAMPLES = CWD.parent / "examples"
TEST_CACHE_DIR = pathlib.Path.home() / "test-cache"
TEST_LIB_DIR = pathlib.Path.home() / "test-libs"

TEST_CALL_TIMEOUT = 5


def __call_executable(app: str, timeout=TEST_CALL_TIMEOUT):
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


def __run_project(project_dir: pathlib.Path, timeout: int = TEST_CALL_TIMEOUT):
    proc = Processor(project_dir)
    proc.run()

    dist_dir = project_dir / "dist"
    os.chdir(dist_dir)
    exe_files = list(_ for _ in dist_dir.glob("*.exe"))

    if not len(exe_files):
        print(f"[#] No exe file found for [{arg.name}].")
        return False

    print(f"\n[#] Running executable: [{exe_files[0].name}].")
    call_result = __call_executable(exe_files[0].as_posix(), timeout=timeout)
    if not call_result:
        print(f"[#] Running failed: [{exe_files[0].name}].")
        return False

    return True


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

    print(f"\nClear environment, {session=}, {exitstatus=}.")


@pytest.fixture
def run_proc():
    """Run processor to build example code and test if it can execute."""

    def runner(
        args: typing.Union[typing.List[pathlib.Path], pathlib.Path],
        timeout: int = TEST_CALL_TIMEOUT,
    ):
        if isinstance(args, pathlib.Path):
            return __run_project(args, timeout=timeout)
        elif isinstance(args, typing.Sequence):
            return all([__run_project(arg, timeout=timeout) for arg in args])
        else:
            print(f"[#] Invalid args: [{args}].")
            return False

    return runner


@pytest.fixture
def dir_examples():
    return DIR_EXAMPLES


@pytest.fixture
def base_helloworld():
    return DIR_EXAMPLES / "base_helloworld"


@pytest.fixture
def base_office():
    return DIR_EXAMPLES / "base_office"


@pytest.fixture
def game_pygame():
    return DIR_EXAMPLES / "game_pygame"


@pytest.fixture
def gui_tkinter():
    return DIR_EXAMPLES / "gui_tkinter"


@pytest.fixture
def gui_pyside2():
    return DIR_EXAMPLES / "gui_pyside2"


@pytest.fixture
def math_matplotlib():
    return DIR_EXAMPLES / "math_matplotlib"


@pytest.fixture
def math_numba():
    return DIR_EXAMPLES / "math_numba"


@pytest.fixture
def math_pandas():
    return DIR_EXAMPLES / "math_pandas"


@pytest.fixture
def math_torch():
    return DIR_EXAMPLES / "math_torch"


@pytest.fixture
def web_bottle():
    return DIR_EXAMPLES / "web_bottle"
