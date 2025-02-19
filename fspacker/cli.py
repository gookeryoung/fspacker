import logging
import pathlib
import subprocess
import time

import click
import toml


class AliasedGroup(click.Group):
    """Custom click group class for aliasing commands."""

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Too many matches: {','.join(sorted(matches))}")


# Group for fspacker command line interface
cli = AliasedGroup(
    name="fspacker",
    help="fspacker command line interface.",
)


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


@cli.command("build", short_help="Build source files.")
@click.option("-d", "--directory", type=click.STRING, default=None, help="Input source file.")
@click.option("--debug/--no-debug", "-D/-ND", default=False, help="Debug mode, show detail information.")
@click.option("-f", "--file", default="", help="Input source file.")
@click.option("-a", "--archive", is_flag=True, help="Archive mode, pack as archive files.")
def build_command(archive: bool, directory: str, file: str, debug: bool):
    if debug:
        logging.basicConfig(level=logging.DEBUG, format="[*] %(message)s")
        logging.info("Debug mode enabled.")
    else:
        logging.basicConfig(level=logging.INFO, format="[*] %(message)s")
        logging.info("Debug mode disabled.")

    from fspacker.conf.settings import settings

    logging.info(f"Current directory: [{directory}].")

    if archive:
        settings.config["mode.archive"] = True

    _proc_directory(directory, file)


@cli.command("update", short_help="Update version for fspacker based on the latest Git tag.")
def update_command():
    pyproject = toml.load("pyproject.toml")

    # Get latest tag from Git
    try:
        tag = (
            subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                stderr=subprocess.STDOUT,
            )
            .strip()
            .decode("utf-8")
        )
        new_version = tag.replace("v", "")
        print(f"Updating version to {new_version} based on the latest tag.")
    except subprocess.CalledProcessError:
        print("No tag found. Skipping version update.")
        return

    # Update pyproject.toml
    with open("pyproject.toml", "w") as f:
        toml.dump(pyproject, f)

    with open("fspacker/__init__.py", "w") as f:
        build_date = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        f.write(f'__version__ = "{new_version}"\n')
        f.write(f'__build_date__ = "{build_date}"\n')

    print(f"Updated version to {new_version}")


@cli.command("version", short_help="Show version information.")
def version_command():
    """Show version information."""

    from fspacker import __build_date__
    from fspacker import __version__

    click.echo(f"fspacker {__version__}, build date: {__build_date__}")


def main():
    cli.main()


if __name__ == "__main__":
    main()
