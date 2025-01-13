import defusedxml


def function_f():
    print("Called from core.module_f, in folder")
    print(defusedxml.__version__)
