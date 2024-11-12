import logging
import pathlib
import zipfile

from fspacker.dirs import get_dist_dir
from fspacker.parser.project import ProjectConfig


def unzip_wheel_file(whl_file: pathlib.Path, output_dir):
    """
    从 .whl 文件中解压指定的文件并将其放到特定目录中。

    :param whl_file: .whl 文件的路径
    :param output_dir: 输出目录
    """

    # 打开 .whl 文件
    with zipfile.ZipFile(whl_file, "r") as zip_ref:
        # 检查目标文件是否存在
        if target_file in zip_ref.namelist():
            # 解压目标文件到输出目录
            zip_ref.extract(target_file, output_dir)
            print(f"Extracted {target_file} to {output_dir}")
        else:
            print(f"{target_file} not found in {whl_file}")


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

        # if lib == "tkinter":
        #     logging.info(
        #         f"解压tkinter库[{PATH_LIB}]->[{packages_dir.parent}]"
        #     )
        #     shutil.unpack_archive(PATH_LIB, packages_dir.parent, "zip")
        #
        # # 对于tkinter库还需要复制依赖库文件
        # logging.info(f"解压依赖库[{lib}]->[{packages_dir}]")
        # shutil.unpack_archive(
        #     DIR_PACKAGE / f"{lib}.zip", packages_dir, "zip"
        # )
