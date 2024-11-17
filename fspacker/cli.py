import argparse
import logging
import pathlib
import time

from fspacker.process import Processor

logging.basicConfig(level=logging.INFO, format="[*] %(message)s")


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
        help="Source root directory",
    )

    args = parser.parse_args()
    zip_mode = args.zip
    directory = pathlib.Path(args.directory)

    if not directory.exists():
        logging.info(f"Directory [{directory}] doesn't exist")
        parser.print_help()
        return

    t0 = time.perf_counter()
    logging.info(f"Start packing, mode: [{'' if zip_mode else 'No-'}Zip]")
    logging.info(f"Source root directory: [{directory}]")

    processor = Processor(directory)
    processor.run()

    logging.info(f"Packing done! Total used: [{time.perf_counter() - t0:.2f}]s.")


if __name__ == "__main__":
    main()
