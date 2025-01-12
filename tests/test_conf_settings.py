import pathlib


def test_user_env_dirs(tmpdir, monkeypatch):
    monkeypatch.setenv("FSPACKER_CACHE", str(tmpdir / ".cache"))

    from fspacker.conf.settings import settings

    assert settings.cache_dir == tmpdir / ".cache"


def test_config(tmpdir):
    from fspacker.conf.settings import settings

    settings.config["mode.offline"] = True
    assert settings.config.get("mode.offline")
    assert settings.config.get("mode.not_exist", None) is None


def test_env_dirs(monkeypatch):
    from fspacker.conf.settings import settings

    assert settings.cache_dir == pathlib.Path("~").expanduser() / ".cache" / "fspacker"
