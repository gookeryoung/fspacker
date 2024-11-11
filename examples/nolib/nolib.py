import os
import sys


def main():
    msg = "Hello from %s" % (os.path.abspath(__file__))
    print(msg)
    print()

    for path in sys.path:
        print(">", path)

    os.MessageBox(msg)
