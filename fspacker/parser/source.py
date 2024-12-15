import ast
import logging
import pathlib
import typing
from io import StringIO

from fspacker.config import TKINTER_LIBS, RES_ENTRIES
from fspacker.parser.base import BaseParser
from fspacker.parser.target import PackTarget, DependInfo
from fspacker.utils.repo import get_builtin_lib_repo

__all__ = ("SourceParser",)


class SourceParser(BaseParser):
    """Parse by source code"""

    def __init__(self, targets: typing.Dict[str, PackTarget], root_dir: pathlib.Path):
        super().__init__(targets, root_dir)

        self.entries: typing.Dict[str, pathlib.Path] = {}
        self.builtins = get_builtin_lib_repo()
        self.code_text = StringIO()
        self.info = DependInfo()

    def parse(self, entry: pathlib.Path):
        with open(entry, encoding="utf-8") as f:
            code = "".join(f.readlines())
            if "def main" in code or "__main__" in code:
                self._parse_content(entry)
                self.targets[entry.stem] = PackTarget(
                    src=entry,
                    deps=self.info.deps,
                    ast=self.info.ast,
                    extra=self.info.extra,
                    code=f"{code}{self.code_text.getvalue()}",
                )
                logging.info(f"Add pack target{self.targets[entry.stem]}")

    def _parse_folder(self, filepath: pathlib.Path) -> DependInfo:
        files: typing.List[pathlib.Path] = list(_ for _ in filepath.iterdir() if _.suffix == ".py")
        for file in files:
            self._parse_content(file)

    def _parse_content(self, filepath: pathlib.Path) -> DependInfo:
        """Analyse ast tree from source code"""
        with open(filepath, encoding="utf-8") as f:
            content = "".join(f.readlines())

        tree = ast.parse(content, filename=filepath)

        local_entries = {_.stem: _ for _ in filepath.parent.iterdir()}
        self.entries.update(local_entries)
        for entry in self.entries.values():
            if entry.stem in RES_ENTRIES:
                self.info.deps.add(entry.stem)

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module is not None:
                    self._parse_import_str(node.module)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self._parse_import_str(alias.name)

    def _parse_import_str(self, import_str: str):
        imports = import_str.split(".")
        filepath_ = self.root.joinpath(*imports)
        if filepath_.is_dir():
            # deps folder
            self._parse_folder(filepath_)
            self.info.deps.add(import_str.split(".")[0].lower())
        elif (source_path := filepath_.with_suffix(".py")).is_file():
            # deps file
            self._parse_content(source_path)
            self.info.deps.add(import_str.split(".")[0].lower())
        else:
            import_name = import_str.split(".")[0].lower()
            if import_name not in self.builtins:
                # ast lib
                self.info.ast.add(import_name.lower())

            # import_name needs tkinter
            if import_name in TKINTER_LIBS:
                self.info.extra.add("tkinter")
