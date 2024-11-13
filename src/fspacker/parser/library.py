import logging
import zipfile

from fspacker.config import IGNORE_SYMBOLS
from fspacker.dirs import get_dist_dir
from fspacker.parser.project import ProjectConfig
from fspacker.repo.depends import fetch_depends_tree
from fspacker.repo.library import LibraryInfo, fetch_libs_repo


def unzip_wheel_file(lib: LibraryInfo, output_dir):
    """从库文件中解压指定的文件并将其放到特定目录中。"""
    lib_repo = fetch_libs_repo()
    dep_tree = fetch_depends_tree()
    dependency = dep_tree.get(lib.package_name)

    with zipfile.ZipFile(lib.filepath, "r") as f:
        for target_file in f.namelist():
            if dependency is not None and hasattr(dependency, "files"):
                relative_path = target_file.replace(f"{lib.package_name}/", "")
                if relative_path not in dependency.files:
                    continue

            if any(_ in target_file for _ in IGNORE_SYMBOLS):
                continue

            f.extract(target_file, output_dir)

    if dependency is not None and hasattr(dependency, "depends"):
        for depend in dependency.depends:
            if (item := lib_repo.get(depend)) is not None:
                unzip_wheel_file(item, output_dir)


def pack_library(target: ProjectConfig):
    packages_dir = get_dist_dir(target.src.parent) / "site-packages"
    if not packages_dir.exists():
        logging.info(f"创建包目录[{packages_dir}]")
        packages_dir.mkdir(parents=True)

    for lib in target.libs:
        exist_folders = list(
            _.stem for _ in packages_dir.iterdir() if _.is_dir()
        )
        if lib.package_name in exist_folders:
            logging.info(f"目录[{packages_dir.name}]下已存在[{lib}]库, 跳过")
            continue

        logging.info(f"解压依赖库[{lib}]->[{packages_dir}]")
        unzip_wheel_file(lib, packages_dir)
