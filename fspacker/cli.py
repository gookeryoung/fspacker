import logging
import pathlib
import subprocess
import time
from dataclasses import dataclass

import click
import toml


def _proc_directory(directory: str, file: str):
    from fspacker.conf.settings import settings

    file_path = pathlib.Path(file)
    dir_path = pathlib.Path(directory) if directory is not None else pathlib.Path.cwd()

    if not dir_path.exists():
        logging.info(f"Directory [{dir_path}] doesn't exist")
        return

    t0 = time.perf_counter()
    logging.info(f"Source root directory: [{dir_path}]")
    logging.info(f"Current mode: [offline={settings.is_offline_mode}]")

    from fspacker.process import Processor

    processor = Processor(dir_path, file_path)
    processor.run()

    logging.info(f"Packing done! Total used: [{time.perf_counter() - t0:.2f}]s.")


@dataclass
class BuildOptions:
    debug: bool
    show_version: bool

    def __repr__(self):
        return f"Build mode: [debug: {self.debug}, version: {self.show_version}]."


@click.group(invoke_without_command=True)
@click.option("--debug", is_flag=True, help="Debug mode, show detail information.")
@click.option(
    "-v", "--version", is_flag=True, help="Debug mode, show detail information."
)
@click.pass_context
def cli(ctx: click.Context, debug: bool, version: bool):
    ctx.obj = BuildOptions(debug=debug, show_version=version)

    if debug:
        logging.basicConfig(level=logging.DEBUG, format="[*] %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="[*] %(message)s")

    logging.info(ctx.obj)

    if version:
        from fspacker import __version__

        logging.info(f"fspacker {__version__}")
        return

    if ctx.invoked_subcommand is None:
        ctx.invoke(build)


@cli.command()
@click.option("-d", "--directory", default=None, help="Input source file.")
@click.option("-f", "--file", default="", help="Input source file.")
@click.option(
    "-a", "--archive", is_flag=True, help="Archive mode, pack as archive files."
)
def build(archive: bool, directory: str, file: str):
    from fspacker.conf.settings import settings

    logging.info(f"Current directory: [{directory}].")

    if archive:
        settings.config["mode.archive"] = True

    _proc_directory(directory, file)


def main():
    cli()


@cli.command()
def update():
    """Update version for fspacker"""

    pyproject = toml.load("pyproject.toml")

    # 获取最新的 Git 标签
    try:
        tag = (
            subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                stderr=subprocess.STDOUT,
            )
            .strip()
            .decode("utf-8")
        )
        new_version = tag.replace("v", "")  # 使用标签作为新版本
        print(f"Updating version to {new_version} based on the latest tag.")
    except subprocess.CalledProcessError:
        # 如果没有标签，打印信息并返回
        print("No tag found. Skipping version update.")
        return

    # 更新 pyproject.toml
    pyproject["tool"]["poetry"]["version"] = new_version
    with open("pyproject.toml", "w") as f:
        toml.dump(pyproject, f)

    # 更新 fspacker/__init__.py
    with open("fspacker/__init__.py", "w") as f:
        f.write(f'__version__ = "{new_version}"')

    print(f"Updated version to {new_version}")


if __name__ == "__main__":
    main()
