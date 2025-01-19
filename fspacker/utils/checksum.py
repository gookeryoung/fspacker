import hashlib
import logging
import pathlib


def calc_checksum(filepath: pathlib.Path, block_size: int = 4096) -> str:
    """Calculate checksum of filepath, using sha256 algorithm.

    :param filepath: Input filepath.
    :param block_size: Read block size, default by 4096.
    :return: String format of checksum.
    """

    hash_method = hashlib.sha256()

    logging.info(f"Calculate checksum for: [{filepath.name}]")

    try:
        with open(filepath, "rb") as file:
            for chunk in iter(lambda: file.read(block_size), b""):
                hash_method.update(chunk)
    except FileNotFoundError:
        logging.error(f"File not found: [{filepath}]")
        return ""
    except IOError as e:
        logging.error(f"IO error occurred while reading file [{filepath}]: {e}")
        return ""

    checksum = hash_method.hexdigest()
    logging.info(f"Checksum is: [{checksum}]")
    return checksum
