from mathtools.algorithms import factorial


def function_g():
    print("Called from core.module_g, in folder")
    for i in range(10):
        print(f"{factorial(i)=}")
