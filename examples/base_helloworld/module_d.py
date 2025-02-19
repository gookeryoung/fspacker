import core
from core import module_g


def function_d():
    print("Called from module_d, single file")
    core.module_g.function_g()
    module_g.function_g()
