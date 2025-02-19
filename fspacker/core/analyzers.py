import dataclasses
import importlib
import importlib.metadata
import json
import logging
import os
import tarfile
import typing
from typing import Dict
from typing import List
from typing import Optional

import packaging.requirements
import stdlib_list
from pkginfo import Wheel

from fspacker.conf.settings import settings

__all__ = [
    "LibraryAnalyzer",
    "LibraryMetaData",
    "BuiltInLibraryAnalyzer",
]


@dataclasses.dataclass
class LibraryMetaData:
    """Metadata for python library analyzer.

    Attributes:
        name (str): The name of the library.
        version (str): The version of the library.
        summary (str): The summary of the library.
        homepage (str): The homepage of the library.
        author (str): The author of the library.
        license (str): The license of the library.
        dependencies (List[str]): The dependencies of the library.

    Examples:

    >>> LibraryMetaData()
    LibraryMetaData(name='Unknown', version='', summary='', homepage='', author='', license='', dependencies=[])
    >>> LibraryMetaData(name="requests")
    LibraryMetaData(name='requests', version='', summary='', homepage='', author='', license='', dependencies=[])
    >>> LibraryMetaData(name="requests", version="2.25.1")
    LibraryMetaData(name='requests', version='2.25.1', summary='', homepage='', author='', license='', dependencies=[])
    >>> LibraryMetaData(name="requests", version="2.25.1", summary="Python HTTP for Humans.")
    LibraryMetaData(name='requests', version='2.25.1', summary='Python HTTP for Humans.', homepage='', author='', license='', dependencies=[])
    >>> LibraryMetaData(name="requests", version="2.25.1", summary="Python HTTP for Humans.", homepage="https://requests.readthedocs.io")
    LibraryMetaData(name='requests', version='2.25.1', summary='Python HTTP for Humans.', homepage='https://requests.readthedocs.io', author='', license='', dependencies=[])
    >>> LibraryMetaData(name="requests", version="2.25.1", summary="Python HTTP for Humans.", homepage="https://requests.readthedocs.io", author="Kenneth Reitz")
    LibraryMetaData(name='requests', version='2.25.1', summary='Python HTTP for Humans.', homepage='https://requests.readthedocs.io', author='Kenneth Reitz', license='', dependencies=[])
    >>> LibraryMetaData(name="requests", version="2.25.1", summary="Python HTTP for Humans.", homepage="https://requests.readthedocs.io", author="Kenneth Reitz", license="Apache-2.0")
    LibraryMetaData(name='requests', version='2.25.1', summary='Python HTTP for Humans.', homepage='https://requests.readthedocs.io', author='Kenneth Reitz', license='Apache-2.0', dependencies=[])
    >>> LibraryMetaData(name="requests", version="2.25.1", summary="Python HTTP for Humans.", homepage="https://requests.readthedocs.io", author="Kenneth Reitz", license="Apache-2.0", dependencies=["urllib3", "chardet"])
    LibraryMetaData(name='requests', version='2.25.1', summary='Python HTTP for Humans.', homepage='https://requests.readthedocs.io', author='Kenneth Reitz', license='Apache-2.0', dependencies=['urllib3', 'chardet'])
    """  # noqa: E501

    name: str = "Unknown"
    version: str = ""
    summary: str = ""
    homepage: str = ""
    author: str = ""
    license: str = ""
    filepath: str = ""
    dependencies: List[str] = dataclasses.field(default_factory=list)


class LibraryAnalyzer:
    """A class for in-depth analysis of specific Python library information."""

    def __init__(self, library_name: str):
        """
        Initialize the LibraryAnalyzer class with the library name.

        Args:
            library_name (str): The name of the library to analyze.
        """
        self.library_name: str = library_name
        self.metadata: LibraryMetaData = self.get_library_metadata()
        self.dependency_tree = self.build_dependency_tree()

    def get_library_metadata(self) -> LibraryMetaData:
        """
        Retrieve metadata for the specified library.

        Returns:
            LibraryMetaData: The metadata of the library.
        """
        try:
            dist = importlib.metadata.distribution(self.library_name)
            raw_dependencies = dist.requires or []
            dependencies: List[str] = self._parse_dependencies(raw_dependencies)

            return LibraryMetaData(
                name=dist.metadata["Name"],
                version=dist.version,
                summary=dist.metadata.get("Summary", ""),
                homepage=dist.metadata.get("Home-page", ""),
                author=dist.metadata.get("Author", ""),
                license=dist.metadata.get("License", ""),
                dependencies=dependencies,
            )

        except importlib.metadata.PackageNotFoundError:
            logging.error(f"Library '{self.library_name}' not found.")
            return LibraryMetaData()
        except Exception as e:
            logging.error(f"Error retrieving metadata for '{self.library_name}': {e}")
            return LibraryMetaData()

    @staticmethod
    def _parse_dependencies(raw_dependencies: List[str]) -> List[str]:
        """
        Parse dependencies to extract only the library names.

        Args:
            raw_dependencies (List[str]): The original list of dependencies.

        Returns:
            List[str]: A list of parsed dependency library names.
        """
        parsed_dependencies = []
        for dep in raw_dependencies:
            try:
                requirement = packaging.requirements.Requirement(dep)
                parsed_dependencies.append(requirement.name)
            except Exception as e:
                logging.warning(f"Error parsing dependency '{dep}': {e}")
        return parsed_dependencies

    def build_dependency_tree(self, depth: int = 1) -> Dict[str, List[str]]:
        """
        Build a dependency tree, recursively fetching secondary dependencies.

        Args:
            depth (int, optional): The recursion depth. Defaults to 1.

        Returns:
            Dict[str, List[str]]: The dependency tree.
        """
        if not self.metadata or not hasattr(self.metadata, "dependencies"):
            return {}

        dependency_tree = {self.library_name: self.metadata.dependencies}

        if depth < 1:
            return dependency_tree

        for dep in self.metadata.dependencies:
            try:
                dep_dist = importlib.metadata.distribution(dep)
                dep_raw_dependencies = dep_dist.requires or []
                dep_dependencies = self._parse_dependencies(dep_raw_dependencies)
                dependency_tree[dep] = dep_dependencies
            except importlib.metadata.PackageNotFoundError:
                logging.warning(f"Dependency library '{dep}' not found.")
                dependency_tree[dep] = []
            except Exception as e:
                logging.error(f"Error retrieving metadata for dependency '{dep}': {e}")
                dependency_tree[dep] = []

        return dependency_tree

    def display_metadata(self) -> None:
        """Display the library's metadata."""

        if not self.metadata:
            print(f"No metadata found for library '{self.library_name}'.")
            return

        print(f"Library Name: {self.metadata.name}")
        print(f"Version: {self.metadata.version}")
        print(f"Summary: {self.metadata.summary}")
        print(f"Homepage: {self.metadata.homepage}")
        print(f"Author: {self.metadata.author}")
        print(f"License: {self.metadata.license}")
        print(f"Dependencies: {', '.join(self.metadata.dependencies)}")

    def analyze_dependencies(self) -> List[str]:
        """
        Analyze and return the library's dependencies.

        Returns:
            List[str]: A list of dependencies.
        """
        return self.metadata.dependencies

    def export_dependency_tree(self, filepath: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Export the dependency tree to a JSON file.

        Args:
            filepath (Optional[str], optional): The path to export the file.
                If None, returns the dictionary. Defaults to None.

        Returns:
            Dict[str, List[str]]: The dependency tree.
        """
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(self.dependency_tree, f, ensure_ascii=False, indent=4)
                logging.info(f"Dependency tree exported to {filepath}")
            except Exception as e:
                logging.error(f"Error exporting dependency tree to {filepath}: {e}")
        return self.dependency_tree

    @staticmethod
    def get_dependencies_from_package(
        package_path: str,
    ) -> typing.Optional[typing.Dict[str, typing.List[str]]]:
        """
        Get the dependency information from a local .whl or .tar.gz file.

        Args:
            package_path (str): The path to the package file.

        Returns:
            Dict[str, List[str]]: A mapping of package names to their dependencies.
        """
        dependencies: typing.Dict[str, typing.List[str]] = {}
        raw_dependencies: typing.Sequence[str] = []
        try:
            if package_path.endswith(".whl"):
                metadata = Wheel(package_path)
                raw_dependencies = metadata.requires_dist or []
            elif package_path.endswith(".tar.gz"):
                with tarfile.open(package_path) as tar:
                    for member in tar.getmembers():
                        if member.name == "METADATA":
                            f = tar.extractfile(member)
                            if f:
                                metadata_content = f.read().decode("utf-8")
                                raw_dependencies = [
                                    line.split(":", 1)[1].strip()
                                    for line in metadata_content.splitlines()
                                    if line.startswith("Requires-Dist:")
                                ]
                                break
            else:
                raise ValueError("Unsupported package format. Please provide a .whl or .tar.gz file.")

            # Parse dependency information
            for requirement in raw_dependencies:
                package_name = packaging.requirements.Requirement(requirement).name
                dependencies.setdefault(package_name, []).append(requirement)

        except Exception as e:
            logging.error(f"Error reading dependencies from package '{package_path}': {e}")

        return dependencies

    @staticmethod
    def analyze_packages_in_directory(
        directory_path: str,
    ) -> Dict[str, Dict[str, List[str]]]:
        """
        Analyze all .whl and .tar.gz files in the specified directory.

        Args:
            directory_path (str): The path to the directory containing package files.

        Returns:
            Dict[str, Dict[str, List[str]]]: A mapping of package names to their dependencies.
        """
        all_dependencies = {}
        try:
            for filename in os.listdir(directory_path):
                if filename.endswith(".whl") or filename.endswith(".tar.gz"):
                    package_path = os.path.join(directory_path, filename)
                    dependencies = LibraryAnalyzer.get_dependencies_from_package(package_path)
                    all_dependencies[filename] = dependencies
        except Exception as e:
            logging.error(f"Error analyzing packages in directory '{directory_path}': {e}")

        return all_dependencies


class BuiltInLibraryAnalyzer:
    """A class for analyzing Python built-in libraries."""

    @staticmethod
    def get_builtin_libraries() -> typing.Set[str]:
        """
        Get a list of all built-in libraries.

        Returns:
            List[str]: A list of built-in library names.
        """
        return set(stdlib_list.stdlib_list(settings.python_ver_short))

    @staticmethod
    def get_library_info(library_name: str) -> typing.Dict[str, str]:
        """
        Get information about a specific built-in library.

        Args:
            library_name (str): The name of the library to analyze.

        Returns:
            Dict[str, str]: A dictionary containing library information.
        """
        info = {}
        try:
            library = importlib.import_module(library_name)
            info["name"] = library_name
            info["version"] = getattr(library, "__version__", "N/A")
            info["doc"] = library.__doc__ or "No documentation available."
        except ImportError:
            info["error"] = f"Library '{library_name}' is not a built-in library."
        except Exception as e:
            info["error"] = str(e)

        return info
