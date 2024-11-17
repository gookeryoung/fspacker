import shutil

from fspacker.process import Processor
from tests.utils import DIR_EXAMPLES


class TestBasePacker:
    def test_create_folder(self):
        root_dir = DIR_EXAMPLES / "ex01_helloworld_console"
        if (root_dir / "dist").exists():
            shutil.rmtree(root_dir / "dist")

        proc = Processor(root_dir=root_dir)
        proc.run()
