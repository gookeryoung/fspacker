import logging
import pathlib
from abc import ABC, abstractmethod

from fspacker.core.commands import commands

__all__ = ["unpack"]


class BaseArchive(ABC):
    """Archive unpacker class."""

    @abstractmethod
    def unpack(self, filepath: pathlib.Path, dest_dir: pathlib.Path):
        pass


class TarArchive(BaseArchive):
    """Tar file unpacker class."""

    def unpack(self, filepath: pathlib.Path, dest_dir: pathlib.Path):
        logging.info(f"Unpacking tar file using pip: [{filepath}]->[{dest_dir}]")
        commands.pip(["install", str(filepath), "-t", str(dest_dir)])


class ArchiveFactory:
    """Archive unpacker class for available extensions."""

    ARCHIVES = dict(
        gz=TarArchive(),
    )
    SUFFIXES = (".whl", ".gz")

    _instance = None

    def unpack(self, filepath: pathlib.Path, dest_dir: pathlib.Path):
        if filepath.exists() and filepath.suffix in self.SUFFIXES:
            logging.info(f"Unpacking file [{filepath}]->[{dest_dir}]")
            archive = self.ARCHIVES.get(filepath.suffix[1:].lower(), None)
            if archive is not None:
                archive.unpack(filepath, dest_dir)
                return

        logging.warning(f"Unpacking file [{filepath}] failed.")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ArchiveFactory()

        return cls._instance


_factory = ArchiveFactory.get_instance()
unpack = _factory.unpack
