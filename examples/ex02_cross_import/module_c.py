from modules.module_a import function_a
from modules.module_b import function_b


def function_c():
    function_a()
    function_b()
    print("Called from module_c, single file")
