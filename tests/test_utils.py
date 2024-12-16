from fspacker.utils.libs import parse_libname
from fspacker.utils.wheel import download_wheel, get_wheel_depends


class TestUtilsLibs:
    LIBS = [
        "orderedset",
        "python-docx",
        "PyYAML",
        "you-get",
        "zstandard",
    ]

    def test_parse_download_libname(self):
        for libname in self.LIBS:
            filepath = download_wheel(libname)
            parse_name = parse_libname(filepath)

            assert parse_name == libname


class TestUtilsWheel:
    def test_download_wheel(self):
        filepath = download_wheel("python-docx")
        libname = parse_libname(filepath)

        assert "python_docx" in filepath.stem
        assert "python-docx" == libname

    def test_get_wheel_depends(self):
        filepath = download_wheel("python-docx")
        requires = get_wheel_depends(filepath)
        assert requires == {"lxml", "typing-extensions"}
