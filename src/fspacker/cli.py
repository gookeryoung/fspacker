import logging
import pathlib
import time
from dataclasses import dataclass

import click

from fspacker.utils.config import ConfigManager


def _proc_directory(file: click.Path, directory: click.Path):
    file = pathlib.Path(file) if file is not None else None
    directory = pathlib.Path(directory)

    if not directory.exists():
        logging.info(f"Directory [{directory}] doesn't exist")
        return

    t0 = time.perf_counter()
    logging.info(f"Source root directory: [{directory}]")

    from fspacker.process import Processor

    processor = Processor(directory, file)
    processor.run()

    logging.info(f"Packing done! Total used: [{time.perf_counter() - t0:.2f}]s.")


@dataclass
class BuildOptions:
    debug: bool
    version: bool

    def __repr__(self):
        return f"Build mode: [debug: {self.debug}]."


@click.group(invoke_without_command=True)
@click.option("--debug", is_flag=True, help="Debug mode, show detail information.")
@click.option("-v", "--version", is_flag=True, help="Debug mode, show detail information.")
@click.pass_context
def cli(ctx: click.Context, debug: bool, version: bool):
    ctx.obj = BuildOptions(debug=debug, version=version)

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
@click.option("-d", "--directory", default=str(pathlib.Path.cwd()), help="Input source file.")
@click.option("-f", "--file", default=None, help="Input source file.")
@click.option("--offline", is_flag=True, help="Offline mode, must set FSPACKER_CACHE and FSPACKER_LIBS first.")
@click.option("-a", "--archive", is_flag=True, help="Archive mode, pack as archive files.")
def build(offline: bool, archive: bool, directory: str, file: str):
    logging.info(f"Current directory: [{directory}].")
    config = ConfigManager.get_instance()

    if offline:
        config["mode.offline"] = True

    if archive:
        config["mode.archive"] = True

    _proc_directory(directory=directory, file=file)


def main():
    cli()


if __name__ == "__main__":
    main()
