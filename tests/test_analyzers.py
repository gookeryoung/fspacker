import json
import os
import shutil
import tarfile
import tempfile
import zipfile
from importlib.metadata import PackageNotFoundError

import pytest

from fspacker.core.analyzers import (
    LibraryAnalyzer,
    LibraryMetaData,
    BuiltInLibraryAnalyzer,
)


@pytest.fixture()
def mock_distribution(mocker):
    """Create a mock distribution object."""

    mock_dist = mocker.MagicMock()
    mock_dist.metadata = {
        "Name": "requests",
        "Summary": "Python HTTP for Humans.",
        "Home-page": "https://requests.readthedocs.io",
        "Author": "Kenneth Reitz",
        "License": "Apache-2.0",
    }
    mock_dist.version = "2.25.1"
    mock_dist.requires = ["urllib3 <3,>=1.21.1", "chardet <6,>=3.0.2"]
    return mock_dist


@pytest.fixture
def mock_dep_dist_urllib3(mocker):
    """Create a mock dependency distribution object."""

    mock_dep_dist = mocker.MagicMock()
    mock_dep_dist.metadata = {
        "Name": "urllib3",
        "Summary": "HTTP library with thread-safe connection pooling, file post, and more.",
        "Home-page": "https://urllib3.readthedocs.io",
        "Author": "Andrey Petrov",
        "License": "MIT",
    }
    mock_dep_dist.version = "1.26.15"
    mock_dep_dist.requires = []
    return mock_dep_dist


@pytest.fixture
def mock_dep_dist_chardet(mocker):
    """Create a mock dependency distribution object."""

    mock_dep_dist = mocker.MagicMock()
    mock_dep_dist.metadata = {
        "name": "chardet",
        "version": "5.2.0",
        "License": "MIT",
        "summary": "Universal encoding detector for Python 3",
        "homepage": "https://github.com/chardet/chardet",
        "author": "Mark Pilgrim",
        "license": "LGPL",
        "dependencies": [],
    }
    return mock_dep_dist


def test_get_library_metadata_found(mocker, mock_distribution):
    """Test retrieving metadata for an existing library."""

    with mocker.patch(
        "importlib.metadata.distribution", return_value=mock_distribution
    ):
        analyzer = LibraryAnalyzer("requests")
        metadata = analyzer.get_library_metadata()

        assert metadata.name == "requests"
        assert metadata.version == "2.25.1"
        assert metadata.summary == "Python HTTP for Humans."
        assert metadata.homepage == "https://requests.readthedocs.io"
        assert metadata.author == "Kenneth Reitz"
        assert metadata.license == "Apache-2.0"
        assert metadata.dependencies == ["urllib3", "chardet"]


def test_get_library_metadata_not_found(mocker):
    """Test retrieving metadata for a non-existent library."""

    with mocker.patch(
        "importlib.metadata.distribution", side_effect=PackageNotFoundError
    ):
        analyzer = LibraryAnalyzer("nonexistent-library")
        metadata = analyzer.get_library_metadata()

        assert metadata == LibraryMetaData()


def test_display_metadata(capsys, mocker, mock_distribution):
    """Test displaying library metadata."""

    with mocker.patch(
        "importlib.metadata.distribution", return_value=mock_distribution
    ):
        analyzer = LibraryAnalyzer("requests")
        analyzer.display_metadata()

        captured = capsys.readouterr()
        expected_output = (
            "Library Name: requests\n"
            "Version: 2.25.1\n"
            "Summary: Python HTTP for Humans.\n"
            "Homepage: https://requests.readthedocs.io\n"
            "Author: Kenneth Reitz\n"
            "License: Apache-2.0\n"
            "Dependencies: urllib3, chardet\n"
        )
        assert captured.out == expected_output


def test_analyze_dependencies(mocker, mock_distribution):
    """Test analyzing library dependencies."""

    with mocker.patch(
        "importlib.metadata.distribution", return_value=mock_distribution
    ):
        analyzer = LibraryAnalyzer("requests")
        dependencies = analyzer.analyze_dependencies()

        assert dependencies == ["urllib3", "chardet"]


def test_build_dependency_tree(
    mocker,
    mock_distribution,
    mock_dep_dist_urllib3,
    mock_dep_dist_chardet,
):
    """Test building the dependency tree."""

    with mocker.patch(
        "importlib.metadata.distribution",
        side_effect=[
            mock_distribution,
            mock_dep_dist_urllib3,
            mock_dep_dist_chardet,
        ],
    ) as _:
        # Configure the main library distribution return
        analyzer = LibraryAnalyzer("requests")
        dependency_tree = analyzer.build_dependency_tree(depth=1)

        expected_tree = {
            "requests": ["urllib3", "chardet"],
            "urllib3": [],
            "chardet": [],
        }

        assert dependency_tree == expected_tree


def test_export_dependency_tree(
    mocker,
    tmp_path,
    mock_distribution,
    mock_dep_dist_urllib3,
    mock_dep_dist_chardet,
):
    """Test exporting the dependency tree to a JSON file."""

    with mocker.patch(
        "importlib.metadata.distribution",
        side_effect=[
            mock_distribution,
            mock_dep_dist_urllib3,
            mock_dep_dist_chardet,
        ],
    ) as _:
        analyzer = LibraryAnalyzer("requests")
        dependency_tree = analyzer.build_dependency_tree(depth=1)

        export_path = tmp_path / "dependency_tree.json"
        analyzer.export_dependency_tree(str(export_path))

        with open(export_path, "r", encoding="utf-8") as f:
            exported_tree = json.load(f)

        assert exported_tree == dependency_tree


def create_mock_whl_file(dependencies):
    """Create a mock .whl file containing specified dependency information."""

    temp_dir = tempfile.mkdtemp()
    whl_path = os.path.join(temp_dir, "mock_package.whl")
    metadata_content = "\n".join(f"Requires-Dist: {dep}" for dep in dependencies)

    with zipfile.ZipFile(whl_path, "w") as whl:
        whl.writestr("METADATA", metadata_content)

    return whl_path


def create_mock_tar_gz_file(dependencies):
    """Create a mock .tar.gz file containing specified dependency information."""

    temp_dir = tempfile.mkdtemp()
    tar_gz_path = os.path.join(temp_dir, "mock_package.tar.gz")
    metadata_content = "\n".join(f"Requires-Dist: {dep}" for dep in dependencies)

    with tarfile.open(tar_gz_path, "w:gz") as tar:
        metadata_file = tempfile.NamedTemporaryFile(delete=False)
        metadata_file.write(metadata_content.encode("utf-8"))
        metadata_file.close()
        tar.add(metadata_file.name, arcname="METADATA")
        os.unlink(metadata_file.name)

    return tar_gz_path


def test_get_dependencies_from_package():
    """Test getting dependency information from .whl and .tar.gz files."""

    dependencies = ["packageA >= 1.0.0", "packageB < 2.0.0"]

    # Test .whl file
    whl_path = create_mock_whl_file(dependencies)
    whl_dependencies = LibraryAnalyzer.get_dependencies_from_package(whl_path)
    assert "packageA" in whl_dependencies
    assert "packageB" in whl_dependencies

    # Test .tar.gz file
    tar_gz_path = create_mock_tar_gz_file(dependencies)
    tar_gz_dependencies = LibraryAnalyzer.get_dependencies_from_package(tar_gz_path)
    assert "packageA" in tar_gz_dependencies
    assert "packageB" in tar_gz_dependencies


def create_mock_packages_directory(dependencies):
    """Create a mock directory with .whl and .tar.gz files containing specified dependency information."""

    temp_dir = tempfile.mkdtemp()

    # Create a mock .whl file
    whl_path = os.path.join(temp_dir, "mock_package.whl")
    metadata_content = "\n".join(f"Requires-Dist: {dep}" for dep in dependencies)
    with zipfile.ZipFile(whl_path, "w") as whl:
        whl.writestr("METADATA", metadata_content)

    # Create a mock .tar.gz file
    tar_gz_path = os.path.join(temp_dir, "mock_package.tar.gz")
    with tarfile.open(tar_gz_path, "w:gz") as tar:
        metadata_file = tempfile.NamedTemporaryFile(delete=False)
        metadata_file.write(metadata_content.encode("utf-8"))
        metadata_file.close()
        tar.add(metadata_file.name, arcname="METADATA")
        os.unlink(metadata_file.name)

    return temp_dir


def test_analyze_packages_in_directory(mocker):
    """Test analyzing all .whl and .tar.gz files in a directory."""

    dependencies = ["packageA >= 1.0.0", "packageB < 2.0.0"]
    temp_dir = create_mock_packages_directory(dependencies)

    # Mock the distribution return values
    mock_dist_pack_a = mocker.MagicMock()
    mock_dist_pack_a.metadata = {
        "Name": "mock_package",
        "Summary": "Mock package for testing.",
        "Home-page": "https://mockpackage.readthedocs.io",
        "Author": "Mock Author",
        "License": "MIT",
    }
    mock_dist_pack_a.version = "0.1.0"
    mock_dist_pack_a.requires = ["packageA >= 1.0.0", "packageB < 2.0.0"]

    with mocker.patch("importlib.metadata.distribution", return_value=mock_dist_pack_a):
        all_dependencies = LibraryAnalyzer.analyze_packages_in_directory(temp_dir)

        assert "mock_package.whl" in all_dependencies
        assert "mock_package.tar.gz" in all_dependencies
        assert all_dependencies["mock_package.whl"] == {
            "packageA": ["packageA >= 1.0.0"],
            "packageB": ["packageB < 2.0.0"],
        }
        assert all_dependencies["mock_package.tar.gz"] == {
            "packageA": ["packageA >= 1.0.0"],
            "packageB": ["packageB < 2.0.0"],
        }

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)


def test_get_builtin_libraries():
    """Test getting the list of built-in libraries."""

    built_in_libraries = BuiltInLibraryAnalyzer.get_builtin_libraries()
    assert isinstance(built_in_libraries, set)
    assert len(built_in_libraries) > 0  # Ensure there are built-in libraries


def test_get_library_info():
    """Test getting information about a specific built-in library."""

    info = BuiltInLibraryAnalyzer.get_library_info("math")
    assert info["name"] == "math"
    assert "doc" in info  # Ensure documentation is present
    assert "version" in info  # Ensure version is present
