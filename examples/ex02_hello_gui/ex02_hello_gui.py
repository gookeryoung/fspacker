import os
import pathlib
import sys


def main():
    sys_path_info = "\n".join(sys.path)
    print(f"系统环境变量:\n{sys_path_info}")

    os.MessageBox(f"来自[{pathlib.Path(__file__)}]的欢迎信息: hello, world!")
