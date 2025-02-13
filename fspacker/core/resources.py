import typing
from functools import cached_property

from fspacker.conf.settings import settings
from fspacker.core.analyzers import (
    BuiltInLibraryAnalyzer,
    LibraryAnalyzer,
)

__all__ = ["resources"]


class Resources:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Resources()

        return cls._instance

    @cached_property
    def libs_repo(self) -> typing.Dict[str, typing.Dict[str, typing.List[str]]]:
        return LibraryAnalyzer.analyze_packages_in_directory(settings.libs_dir)

    @cached_property
    def builtin_repo(self) -> typing.Set[str]:
        return BuiltInLibraryAnalyzer.get_builtin_libraries()


resources = Resources.get_instance()
