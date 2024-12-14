import dataclasses
import logging
import pathlib
import typing

__all__ = [
    "LibraryInfo",
]


@dataclasses.dataclass
class LibraryInfo:
    package_name: str
    version: typing.List[str]
    build_tag: str
    abi_tag: str
    platform_tag: str
    filepath: pathlib.Path

    def __repr__(self):
        return f"{self.package_name}-{self.version}"

    @staticmethod
    def from_path(path: pathlib.Path):
        try:
            if path.suffix in ".whl":
                package_name, *version, build_tag, abi_tag, platform_tag = path.stem.split("-")
                return LibraryInfo(
                    package_name=package_name,
                    version=version,
                    build_tag=build_tag,
                    abi_tag=abi_tag,
                    platform_tag=platform_tag,
                    filepath=path,
                )
            elif path.suffix in ".tar.gz":
                package_name, *version = path.stem.split("-")
                return LibraryInfo(
                    package_name=package_name,
                    version=version,
                    build_tag=None,
                    abi_tag=None,
                    platform_tag=None,
                    filepath=path
                )
            else:
                raise ValueError(f"Unsupported file type: {path.suffix}")
        except ValueError as e:
            logging.error(f"[!!!]Invalid path: {path}, error: {e}")
            return None
