import logging
import os
import pathlib
import typing

logging.basicConfig(level=logging.INFO, format="[*] %(message)s")

__all__ = (
    "get_config_filepath",
    "get_embed_archive_name",
    "get_assets_dir",
    "get_depends_filepath",
    "get_embed_dir",
    "get_embed_filepath",
    "get_lib_dir",
    "get_dist_dir",
    "get_runtime_dir",
)

_cache_dir: typing.Optional[pathlib.Path] = None
_embed_dir: typing.Optional[pathlib.Path] = None
_lib_dir: typing.Optional[pathlib.Path] = None
_assets_dir: typing.Optional[pathlib.Path] = None
_config_path: typing.Optional[pathlib.Path] = None
_depends_path: typing.Optional[pathlib.Path] = None
_embed_path: typing.Optional[pathlib.Path] = None
_python_ver: typing.Optional[str] = None
_python_ver_major: typing.Optional[str] = None
_arch: typing.Optional[str] = None
_archive_file: typing.Optional[str] = None


def get_dist_dir(project_dir: pathlib.Path) -> pathlib.Path:
    dist_dir = project_dir / "dist"
    if not dist_dir.exists():
        dist_dir.mkdir(parents=True)

    return dist_dir


def get_runtime_dir(project_dir: pathlib.Path) -> pathlib.Path:
    return get_dist_dir(project_dir) / "runtime"
