import os


class TestProcess:
    def test_base_examples(self, base_examples, run_proc):
        assert run_proc(base_examples)

    def test_base_examples_with_tmp_cache(
        self, base_examples, run_proc, tmpdir
    ):
        os.environ["FSPACKER_LIBS"] = str(tmpdir / "libs-repo")
        os.environ["FSPACKER_CACHE"] = str(tmpdir / ".cache")
        print(f"{os.getenv('FSPACKER_CACHE')=}")

        assert run_proc(base_examples)

    def test_game_examples(self, game_examples, run_proc):
        assert run_proc(game_examples)

    def test_gui_examples(self, gui_examples, run_proc):
        assert run_proc(gui_examples)

    def test_math_examples(self, math_examples, run_proc):
        assert run_proc(math_examples)

    def test_web_examples(self, web_examples, run_proc):
        assert run_proc(web_examples)
