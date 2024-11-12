import argparse
import logging
import pathlib
import time

from fspacker.parser.source import SourceParser
from fspacker.repo.depends import fetch_depends_tree
from fspacker.repo.library import fetch_libs_repo, get_libs_std
from fspacker.repo.runtime import fetch_runtime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--simplify", type=bool, default=True, help="精简模式"
    )
    parser.add_argument(
        "-z", "--zip", type=bool, default=False, help="压缩模式"
    )
    parser.add_argument(
        "-d",
        "--dir",
        dest="directory",
        type=str,
        default=str(pathlib.Path.cwd()),
        help="源代码路径",
    )

    args = parser.parse_args()
    simplify = args.simplify
    zip_mode = args.zip
    directory = pathlib.Path(args.directory)

    t0 = time.perf_counter()
    logging.info("启动打包")
    logging.info(
        f"模式: [{'' if simplify else '非'}精简, {'' if zip_mode else '非'}压缩]"
    )
    logging.info(f"源代码路径: [{directory}]")

    fetch_runtime()
    fetch_libs_repo()
    fetch_depends_tree()
    get_libs_std()

    parser = SourceParser(directory, directory)
    parser.pack()

    logging.info(f"打包完成, 总共用时: {time.perf_counter() - t0:.2f}s.")


if __name__ == "__main__":
    main()
