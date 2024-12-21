import pathlib

from fspacker.utils.config import get_config_manager
from fspacker.utils.libs import (
    get_lib_meta_depends,
    get_lib_meta_name,
    get_zip_meta_data,
    unpack_zipfile,
)
from fspacker.utils.url import (
    get_fastest_embed_url,
    get_fastest_pip_url,
)
from fspacker.utils.wheel import download_wheel, remove_wheel


class TestUtilsLibs:
    LIB_NAMES = [
        "orderedset",
        "python-docx",
        "pyyaml",
        "you-get",
        "zstandard",
    ]

    def test_get_lib_meta_name(self):
        for lib_name in self.LIB_NAMES:
            lib_file = download_wheel(lib_name)
            parse_name = get_lib_meta_name(lib_file)

            assert parse_name == lib_name

    def test_get_lib_meta_name_fail(self):
        try:
            lib_name = get_lib_meta_name(filepath=None)
        except ValueError:
            pass
        else:
            assert lib_name is None

    def test_get_zip_meta_data(self):
        for lib_name in self.LIB_NAMES:
            lib_file = download_wheel(lib_name)
            name, version = get_zip_meta_data(lib_file)
            assert name == lib_name

    def test_get_zip_meta_data_fail(self):
        name, version = get_zip_meta_data(pathlib.Path("sample_file.zip"))
        assert name == ""
        assert version == ""

    def test_get_lib_depends(self):
        lib_file = download_wheel("python-docx")
        requires = get_lib_meta_depends(lib_file)
        assert requires == {"lxml", "typing-extensions"}

    def test_get_lib_depends_fail(self):
        try:
            lib_name = get_lib_meta_depends(filepath=None)
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
        lib_name = get_lib_meta_name(lib_file)

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
        config = get_config_manager()
        config["fastest_pip_url"] = None
        config["fastest_embed_url"] = None
        self.test_get_fastest_urls_from_json()
