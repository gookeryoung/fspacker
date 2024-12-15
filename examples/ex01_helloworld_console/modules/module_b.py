from core.module_e import function_e
from core.module_f import function_f
from module_d import function_d


def function_b():
    print("Called from module_b, in folder")
    function_d()
    function_e()
    function_f()
