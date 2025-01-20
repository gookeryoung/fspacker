import dataclasses
import importlib.metadata
import json
import logging
from typing import List, Dict, Optional

import packaging.requirements

__all__ = ["LibraryAnalyzer", "LibraryMetaData"]


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
    """

    name: str = "Unknown"
    version: str = ""
    summary: str = ""
    homepage: str = ""
    author: str = ""
    license: str = ""
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

    def export_dependency_tree(
        self, filepath: Optional[str] = None
    ) -> Dict[str, List[str]]:
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
