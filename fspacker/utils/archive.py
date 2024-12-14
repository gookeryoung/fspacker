import logging
import pathlib
import subprocess


def unpack_archive(archive_path: pathlib.Path, dest_dir: pathlib.Path):
    logging.info(f"Unpacking file [{archive_path.name}] -> [{dest_dir}]")
    subprocess.call(
        [
            "python",
            "-m",
            "pip",
            "install",
            archive_path.as_posix(),
            "-t",
            dest_dir.as_posix(),
            "--no-index",
            "--find-links",
            str(archive_path.parent),
        ],
    )
