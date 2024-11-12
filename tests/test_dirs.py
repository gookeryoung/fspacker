import os
import pathlib
import platform
import sys

from fspacker.dirs import (
    get_embed_archive_name,
    get_python_ver,
    get_python_ver_major,
)


def test_get_py_ver():
    ver = get_python_ver()
    assert ver == "".join(sys.version[:5])


def test_get_py_ver_major():
    ver = get_python_ver_major()
    assert ver == "".join(sys.version[:3])


def test_get_arch():
    arch_name = get_embed_archive_name()
    machine = (
        "amd64"
        if platform.uname().machine.lower() in ["x86_64", "amd64"]
        else "x86"
    )
    assert arch_name == f"python-{sys.version[:5]}-embed-{machine}.zip"


def test_cached_dir():
    os.environ["FSPACKER_CACHE_DIR"] = pathlib.Path()
