import argparse
import logging
import pathlib
import time

from fspacker.process import Processor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-z",
        "--zip",
        type=bool,
        default=False,
        help="Zip mode, pack as zip files.",
    )
    parser.add_argument(
        "--debug",
        type=bool,
        default=False,
        help="Debug mode, show detail information",
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
    zip_mode = args.zip
    directory = pathlib.Path(args.directory)

    t0 = time.perf_counter()
    logging.info(f"启动打包, 模式: [{'' if zip_mode else '非'}压缩]")
    logging.info(f"源代码路径: [{directory}]")

    processor = Processor(directory)
    processor.run()

    # fetch_runtime()
    # fetch_libs_repo()
    # get_libs_std()
    #
    # parser = SourceParser(directory, directory)
    # parser.pack()

    logging.info(f"打包完成, 总共用时: {time.perf_counter() - t0:.2f}s.")


if __name__ == "__main__":
    main()
