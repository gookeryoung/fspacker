import logging
import pathlib
import subprocess
import zipfile

from fspacker.common import BuildTarget
from fspacker.config import IGNORE_SYMBOLS
from fspacker.dirs import get_dist_dir, get_lib_dir
from fspacker.packer.base import BasePacker
from fspacker.repo.depends import fetch_depends_tree
from fspacker.repo.library import fetch_libs_repo


def unzip_lib_file(lib: str, output_dir):
    """从库文件中解压指定的文件并将其放到特定目录中。"""
    lib_repo = fetch_libs_repo()
    dep_tree = fetch_depends_tree()
    lib_info = lib_repo.get(lib)
    dependency = dep_tree.get(lib)
    lib_dir = get_lib_dir()

    if lib_info is not None:
        with zipfile.ZipFile(lib_info.filepath, "r") as f:
            for target_file in f.namelist():
                if dependency is not None and hasattr(dependency, "files"):
                    relative_path = target_file.replace(
                        f"{lib_info.package_name}/", ""
                    )
                    if relative_path not in dependency.files:
                        continue

                if any(_ in target_file for _ in IGNORE_SYMBOLS):
                    continue

                f.extract(target_file, output_dir)

    if dependency is not None and hasattr(dependency, "depends"):
        for depend in dependency.depends:
            if lib_repo.get(depend) is None:
                download_library(depend, lib_dir)
                logging.info(f"下载依赖库[{depend}]->[{lib_dir}]")

            unzip_lib_file(depend, output_dir)


def download_library(lib: str, lib_dir: pathlib.Path):
    subprocess.call(
        [
            "python",
            "-m",
            "pip",
            "download",
            lib,
            "--no-deps",
            "-d",
            str(lib_dir),
        ],
    )


class LibraryPacker(BasePacker):
    def pack(self, target: BuildTarget):
        packages_dir = get_dist_dir(target.src.parent) / "site-packages"
        libs_repo = fetch_libs_repo()
        lib_dir = get_lib_dir()

        if not packages_dir.exists():
            logging.info(f"创建包目录[{packages_dir}]")
            packages_dir.mkdir(parents=True)

        for lib in target.ast:
            exist_folders = list(
                _.stem for _ in packages_dir.iterdir() if _.is_dir()
            )
            if lib in exist_folders:
                logging.info(
                    f"目录[{packages_dir.name}]下已存在[{lib}]库, 跳过"
                )
                continue

            if lib not in libs_repo:
                logging.info(f"库目录中未找到[{lib}]")
                download_library(lib, lib_dir)
                logging.info(f"下载依赖库[{lib}]->[{lib_dir}]")

            logging.info(f"解压依赖库[{lib}]->[{packages_dir}]")
            unzip_lib_file(lib, packages_dir)
