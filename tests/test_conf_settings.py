import pathlib
import shutil


def test_embed_file():
    import platform
    import sys

    from fspacker.conf.settings import settings

    version = sys.version.split(" ")[0]
    assert settings.embed_filename == f"python-{version}-embed-{platform.machine().lower()}.zip"


def test_dirs():
    from fspacker.conf.settings import settings

    assert settings.cache_dir == pathlib.Path("~").expanduser() / ".cache" / "fspacker"
    assert settings.libs_dir == pathlib.Path("~").expanduser() / ".cache" / "fspacker" / "libs-repo"


def test_user_dirs(tmpdir, monkeypatch):
    monkeypatch.setenv("FSPACKER_CACHE", str(tmpdir / ".cache"))
    monkeypatch.setenv("FSPACKER_LIBS", str(tmpdir / ".cache" / "libs-repo"))

    from fspacker.conf.settings import settings

    assert settings.cache_dir == tmpdir / ".cache"
    assert settings.libs_dir == tmpdir / ".cache" / "libs-repo"


def test_clear_dirs(tmpdir, monkeypatch):
    monkeypatch.setenv("FSPACKER_CACHE", str(tmpdir / ".cache"))
    if (tmpdir / ".cache").exists():
        shutil.rmtree(tmpdir / ".cache")

    from fspacker.conf.settings import settings

    assert settings.cache_dir == tmpdir / ".cache"


def test_config():
    from fspacker.conf.settings import settings

    settings.is_offline_mode = False
    assert settings.config.get("mode.not_exist", None) is None
    assert settings.config.get("mode.debug", None) is None
