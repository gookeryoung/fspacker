import dataclasses
import pathlib

from pkginfo import Distribution
from fspacker.utils.zip import get_zip_meta_data

@dataclasses.dataclass
class LibraryInfo:
    meta_data: Distribution
    filepath: pathlib.Path

    def __repr__(self):
        return f"{self.meta_data.name}-{self.meta_data.version}"

    @staticmethod
    def from_filepath(filepath: pathlib.Path):
        name, version = get_zip_meta_data(filepath)
        lib_info = LibraryInfo(filepath=filepath, meta_data=Distribution())
        lib_info.meta_data.name = name
        lib_info.meta_data.version = version
        return lib_info