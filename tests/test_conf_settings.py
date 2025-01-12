from fspacker.conf.settings import settings


class TestSettings:
    def test_dirs(self):
        pass

    def test_config(self, tmpdir):
        config = settings.CONFIG
        config["mode.offline"] = True
        assert config.get("mode.offline")
        assert config.get("mode.not_exist", None) is None
