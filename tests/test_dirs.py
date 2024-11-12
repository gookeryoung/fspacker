import pathlib
import platform
import shutil
import sys

from fspacker.dirs import (
    _get_cached_dir,
    get_assets_dir,
    get_config_filepath,
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


def test_cached_dir_default():
    cached_dir_expect = pathlib.Path().home() / ".cache" / "fspacker"
    if cached_dir_expect.exists():
        shutil.rmtree(str(cached_dir_expect))

    cached_dir = _get_cached_dir()
    assert str(cached_dir) == str(cached_dir_expect)


def test_get_config_filepath():
    config = get_config_filepath()
    assert config.name == "config.json"


def test_get_assets_dir():
    assets_dir = get_assets_dir()
    assert "assets" in str(assets_dir)

    filenames = list(_.name for _ in assets_dir.iterdir())
    assert all(
        _ in filenames for _ in ("gui.exe", "console.exe", "depends.toml")
    )
