class TestProcess:
    def test_base_helloworld(self, base_helloworld, run_proc):
        assert run_proc(base_helloworld)

    def test_base_office(self, base_office, run_proc):
        assert run_proc(base_office)

    def test_base_helloworld_tmp_cache(self, base_helloworld, run_proc, tmpdir):
        from fspacker.utils.config import ConfigManager

        config = ConfigManager.get_instance()
        config["FSPACKER_CACHE"] = str(tmpdir / "cache")
        assert run_proc(base_helloworld)

    def test_game_pygame(self, game_pygame, run_proc):
        assert run_proc(game_pygame)

    def test_gui_tkinter_run_twice(self, gui_tkinter, run_proc):
        assert run_proc([gui_tkinter, gui_tkinter])

    def test_gui_pyside2(self, gui_pyside2, run_proc):
        assert run_proc(gui_pyside2)

    def test_math_matplotlib(self, math_matplotlib, run_proc):
        assert run_proc(math_matplotlib)

    def test_math_numba(self, math_numba, run_proc):
        assert run_proc(math_numba)

    def test_math_pandas(self, math_pandas, run_proc):
        assert run_proc(math_pandas)

    def test_math_torch(self, math_torch, run_proc):
        assert run_proc(math_torch)

    def test_web_bottle(self, web_bottle, run_proc):
        assert run_proc(web_bottle)
