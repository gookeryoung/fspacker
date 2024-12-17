import os
import pathlib

from fspacker.utils.libs import get_lib_depends, get_lib_name, unpack_zipfile
from fspacker.utils.persist import update_json_values
from fspacker.utils.url import (
    get_fastest_embed_url,
    get_fastest_pip_url,
)
from fspacker.utils.wheel import download_wheel, remove_wheel


class TestUtilsLibs:
    LIB_NAMES = [
        "orderedset",
        "python-docx",
        "PyYAML",
        "you-get",
        "zstandard",
    ]

    def test_get_lib_name(self):
        for lib_name in self.LIB_NAMES:
            lib_file = download_wheel(lib_name)
            parse_name = get_lib_name(lib_file)

            assert parse_name == lib_name

    def test_get_lib_name_fail(self):
        try:
            lib_name = get_lib_name(filepath=None)
        except ValueError:
            pass
        else:
            assert lib_name is None

    def test_get_lib_depends(self):
        lib_file = download_wheel("python-docx")
        requires = get_lib_depends(lib_file)
        assert requires == {"lxml", "typing-extensions"}

    def test_get_lib_depends_fail(self):
        try:
            lib_name = get_lib_depends(filepath=None)
        except ValueError:
            pass
        else:
            assert lib_name is None

    def test_unpack_zipfile(self, tmpdir):
        lib_file = download_wheel("orderedset")
        unpack_zipfile(lib_file, tmpdir)
        tmp_folder = pathlib.Path(tmpdir) / "orderedset"
        assert tmp_folder.is_dir()


class TestUtilsWheel:
    def test_download_wheel(self):
        lib_file = download_wheel("python-docx")
        lib_name = get_lib_name(lib_file)

        assert "python_docx" in lib_file.stem
        assert "python-docx" == lib_name

    def test_re_download_wheel(self):
        remove_wheel("python-docx")
        self.test_download_wheel()


class TestUrl:
    def test_get_fastest_urls_from_json(self):
        pip_url = get_fastest_pip_url()
        embed_url = get_fastest_embed_url()
        assert "aliyun" in pip_url
        assert "huawei" in embed_url

    def test_get_fastest_urls(self):
        update_json_values(
            dict(
                fastest_pip_url=None,
                fastest_embed_url=None,
            )
        )
        self.test_get_fastest_urls_from_json()
