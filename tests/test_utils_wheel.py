from fspacker.process import Processor
from tests.utils import DIR_EXAMPLES


class TestUtilsWheel:
    def test_download_wheel(self):
        root_dir = DIR_EXAMPLES / "ex04_pyside_complex"
        proc = Processor(root_dir)
        proc.run()
