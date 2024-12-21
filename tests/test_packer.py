import shutil

from fspacker.process import Processor


class TestBasePacker:
    def test_create_folder(self, base_examples):
        for example in base_examples:
            dist_dir = example / "dist"
            if dist_dir.exists():
                shutil.rmtree(dist_dir)

            proc = Processor(example)
            proc.run()

            assert dist_dir.exists()
