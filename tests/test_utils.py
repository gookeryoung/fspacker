from fspacker.utils.libs import get_lib_name, get_lib_depends
from fspacker.utils.wheel import download_wheel, remove_wheel


class TestUtilsLibs:
    LIBS = [
        "orderedset",
        "python-docx",
        "PyYAML",
        "you-get",
        "zstandard",
    ]

    def test_get_lib_name(self):
        for libname in self.LIBS:
            filepath = download_wheel(libname)
            parse_name = get_lib_name(filepath)

            assert parse_name == libname

    def test_get_lib_name_fail(self):
        try:
            libname = get_lib_name(filepath=None)
        except ValueError:
            pass
        else:
            assert libname is None

    def test_get_lib_depends(self):
        filepath = download_wheel("python-docx")
        requires = get_lib_depends(filepath)
        assert requires == {"lxml", "typing-extensions"}

    def test_get_lib_depends_fail(self):
        try:
            libname = get_lib_depends(filepath=None)
        except ValueError:
            pass
        else:
            assert libname is None


class TestUtilsWheel:
    def test_download_wheel(self):
        filepath = download_wheel("python-docx")
        libname = get_lib_name(filepath)

        assert "python_docx" in filepath.stem
        assert "python-docx" == libname

    def test_re_download_wheel(self):
        remove_wheel("python-docx")
        filepath = download_wheel("python-docx")
        libname = get_lib_name(filepath)

        assert "python_docx" in filepath.stem
        assert "python-docx" == libname
