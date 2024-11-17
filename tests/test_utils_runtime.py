from fspacker.packer.runtime import _check_url_access_time


class TestUtilsRuntime:
    def test_check_url_overtime(self):
        assert _check_url_access_time("www.test=code-123.com") == -1
