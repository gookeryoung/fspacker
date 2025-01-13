import logging
import pathlib
import time
from dataclasses import dataclass

import click

from fspacker.conf.settings import settings


def _proc_directory(directory: str, file: str):
    file_path = pathlib.Path(file)
    dir_path = pathlib.Path(directory) if directory is not None else pathlib.Path.cwd()

    if not dir_path.exists():
        logging.info(f"Directory [{dir_path}] doesn't exist")
        return

    t0 = time.perf_counter()
    logging.info(f"Source root directory: [{dir_path}]")

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
    "--offline",
    is_flag=True,
    help="Offline mode, must set FSPACKER_CACHE and FSPACKER_LIBS first.",
)
@click.option(
    "-a", "--archive", is_flag=True, help="Archive mode, pack as archive files."
)
def build(offline: bool, archive: bool, directory: str, file: str):
    logging.info(f"Current directory: [{directory}].")

    if offline:
        settings.config["mode.offline"] = True

    if archive:
        settings.config["mode.archive"] = True

    _proc_directory(directory, file)


def main():
    cli()


if __name__ == "__main__":
    main()
