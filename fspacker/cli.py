import argparse
import logging
import pathlib
import time

from fspacker.process import Processor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        nargs="?",
        help="Input source file",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Show version",
    )
    parser.add_argument(
        "-z",
        "--zip",
        type=bool,
        default=False,
        help="Zip mode, pack as zip files.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Debug mode, show detail information",
    )
    parser.add_argument(
        "-d",
        "--dir",
        dest="directory",
        type=str,
        default=str(pathlib.Path.cwd()),
        help="Source root directory",
    )

    args = parser.parse_args()
    file = pathlib.Path(args.file) if args.file else None
    zip_mode = args.zip
    directory = pathlib.Path(args.directory)
    show_version = args.version
    show_debug = args.debug

    if show_version:
        from fspacker import __version__

        logging.info(f"fspacker {__version__}")
        return

    if show_debug:
        logging.basicConfig(level=logging.DEBUG, format="[*] %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="[*] %(message)s")

    if not directory.exists():
        logging.info(f"Directory [{directory}] doesn't exist")
        parser.print_help()
        return

    t0 = time.perf_counter()
    logging.info(f"Start packing, mode: [{'' if zip_mode else 'No-'}Zip]")
    logging.info(f"Source root directory: [{directory}]")

    processor = Processor(directory, file)
    processor.run()

    logging.info(
        f"Packing done! Total used: [{time.perf_counter() - t0:.2f}]s."
    )


if __name__ == "__main__":
    main()
