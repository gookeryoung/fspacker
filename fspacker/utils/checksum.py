import hashlib
import logging
import pathlib


def calc_checksum(filepath: pathlib.Path, block_size: int = 4096) -> str:
    """Calculate checksum of filepath, using md5 algorithm.

    :param filepath: Input filepath.
    :param block_size: Read block size, default by 4096.
    :return: String format of checksum.
    """

    hash_method = hashlib.sha256()

    logging.info(f"Calculate checksum for: [{filepath.name}]")
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(block_size), b""):
            hash_method.update(chunk)

    logging.info(f"Checksum is: [{hash_method.hexdigest()}]")
    return str(hash_method.hexdigest())
