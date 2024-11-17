import logging
import os
import pathlib
import subprocess

from fspacker.config import TEST_CALL_TIMEOUT

CWD = pathlib.Path(__file__).parent
DIR_EXAMPLES = CWD.parent / "examples"


def exec_dist_dir(dist_dir: pathlib.Path):
    os.chdir(dist_dir)
    exe_files = list(_ for _ in dist_dir.glob("*.exe"))

    if not len(exe_files):
        return False

    try:
        subprocess.run([exe_files[0]], timeout=TEST_CALL_TIMEOUT)
    except subprocess.CalledProcessError as e:
        logging.error(e)
        return False
    except subprocess.TimeoutExpired:
        return True
    else:
        return True