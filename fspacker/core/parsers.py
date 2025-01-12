import ast
import logging
import pathlib
import typing
from abc import ABC, abstractmethod
from io import StringIO

from fspacker.conf.settings import settings
from fspacker.core.resources import resources
from fspacker.core.target import PackTarget, Dependency

__all__ = ["parser_factory"]


class BaseParser(ABC):
    """Base class for parsers"""

    @abstractmethod
    def parse(self, entry: pathlib.Path, root_dir: pathlib.Path):
        pass


class FolderParser(BaseParser):
    """Parser for folders"""

    def parse(self, entry: pathlib.Path, root_dir: pathlib.Path):
        if entry.stem.lower() in settings.ignore_symbols:
            logging.info(f"Skip parsing folder: [{entry.stem}]")
            return

        for k, v in parser_factory.TARGETS.items():
            if entry.stem in v.code:
                v.sources.add(entry.stem)
                logging.info(f"Update pack target: {v}")


class SourceParser(BaseParser):
    """Parse by source code"""

    root_dir: pathlib.Path
    entries: typing.Dict[str, pathlib.Path]
    info: Dependency
    code_text: StringIO

    def parse(self, entry: pathlib.Path, root_dir: pathlib.Path) -> None:
        self.root_dir = root_dir
        self.entries = {}
        self.info = Dependency()
        self.code_text = StringIO()

        with open(entry, encoding="utf-8") as f:
            code = "".join(f.readlines())
            if "def main" in code or "__main__" in code:
                self._parse_content(entry)
                parser_factory.TARGETS[entry.stem] = PackTarget(
                    src=entry,
                    depends=self.info,
                    code=f"{code}{self.code_text.getvalue()}",
                )
                logging.info(f"Add pack target{parser_factory.TARGETS[entry.stem]}")

    def _parse_folder(self, filepath: pathlib.Path) -> None:
        files: typing.List[pathlib.Path] = list(
            _ for _ in filepath.iterdir() if _.suffix == ".py"
        )
        for file in files:
            self._parse_content(file)

    def _parse_content(self, filepath: pathlib.Path) -> None:
        """Analyse ast tree from source code"""
        with open(filepath, encoding="utf-8") as f:
            content = "".join(f.readlines())

        tree = ast.parse(content, filename=filepath)
        local_entries = {_.stem: _ for _ in filepath.parent.iterdir()}
        self.entries.update(local_entries)
        for entry in self.entries.values():
            if entry.stem in settings.res_entries:
                self.info.sources.add(entry.stem)

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module is not None:
                    self._parse_import_str(node.module)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self._parse_import_str(alias.name)

    def _parse_import_str(self, import_str: str) -> None:
        imports = import_str.split(".")
        filepath_ = self.root_dir.joinpath(*imports)
        if filepath_.is_dir():
            # deps folder
            self._parse_folder(filepath_)
            self.info.sources.add(import_str.split(".")[0])
        elif (source_path := filepath_.with_suffix(".py")).is_file():
            # deps file
            self._parse_content(source_path)
            self.info.sources.add(import_str.split(".")[0])
        else:
            import_name = import_str.split(".")[0].lower()
            if import_name not in resources.BUILTIN_REPO:
                # ast lib
                self.info.libs.add(import_name)

            # import_name needs tkinter
            if import_name in settings.tkinter_libs:
                self.info.extra.add("tkinter")


class ParserFactory:
    PARSERS: typing.Dict[str, BaseParser] = {}
    TARGETS: typing.Dict[str, PackTarget] = {}

    _instance = None

    def parse(self, entry: pathlib.Path, root_dir: pathlib.Path):
        if entry.is_dir():
            parser = self.PARSERS.get("folder", None)
        elif entry.is_file() and entry.suffix in ".py":
            parser = self.PARSERS.get("source", None)
        else:
            parser = None

        if parser is not None:
            parser.parse(entry, root_dir)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ParserFactory()
            cls._instance.PARSERS = dict(
                folder=FolderParser(),
                source=SourceParser(),
            )

        return cls._instance


parser_factory = ParserFactory.get_instance()
