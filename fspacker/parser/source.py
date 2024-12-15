import ast
import logging
import pathlib
import typing
from io import StringIO

from fspacker.config import TKINTER_LIBS
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

        for node in ast.walk(tree):
            import_name: typing.Optional[str] = None

            if isinstance(node, ast.ImportFrom):
                if node.module is not None:
                    import_name = node.module.split(".")[0].lower()
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    import_name = alias.name.split(".")[0].lower()

            if import_name is not None:
                # import from local files or package folders
                if import_name in self.entries:
                    self.info.deps.add(import_name)

                    entry_path = self.entries.setdefault(import_name, None)
                    if entry_path and filepath.parent.resolve() != entry_path.resolve():
                        if entry_path.is_file():
                            if entry_path.parent.stem not in self.info.deps:
                                with open(entry_path, encoding="utf-8") as f:
                                    self.code_text.write("".join(f.readlines()))
                                self._parse_content(entry_path)

                        elif entry_path.is_dir():
                            self._parse_folder(entry_path)

                elif import_name not in self.builtins:
                    self.info.ast.add(import_name.lower())

                # import_name needs tkinter
                if import_name in TKINTER_LIBS:
                    self.info.extra.add("tkinter")
