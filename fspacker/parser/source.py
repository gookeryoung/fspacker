import logging
import pathlib
import typing


__all__ = ("SourceParser",)

import stdlib_list

from fspacker.config import PYTHON_VER_SHORT, TKINTER_LIBS
from fspacker.parser.base import BaseParser

import ast
from fspacker.common import PackTarget, PackConfig


class SourceParser(BaseParser):
    """Parse by source code"""

    STD_LIBS: typing.Set[str] = set()

    def __init__(self, config: PackConfig, root_dir: pathlib.Path):
        super().__init__(config, root_dir)

        self._parse_std_libs()

    def parse(self, entry: pathlib.Path):
        with open(entry, encoding="utf-8") as f:
            code = "".join(f.readlines())
            if "def main" in code or "__main__" in code:
                ast_tree, extra, deps = self._parse_ast(code, entry)
                self.config.targets[entry.stem] = PackTarget(
                    src=entry,
                    deps=deps,
                    ast=ast_tree,
                    extra=extra,
                    code=code,
                )
                logging.info(f"Add pack target{self.config.targets[entry.stem]}")

    def _parse_ast(self, content: str, filepath: pathlib.Path) -> typing.Set[str]:
        """Analyse ast tree from source code"""

        tree = ast.parse(content, filename=filepath)
        entries = list(_.stem for _ in filepath.parent.iterdir())
        imports = set()
        extra = set()
        deps = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                import_name = node.module.split(".")[0].lower()
                if import_name in entries:
                    deps.add(import_name)
                elif import_name not in self.STD_LIBS:
                    imports.add(import_name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    import_name = alias.name.split(".")[0].lower()
                    if import_name in entries:
                        deps.add(import_name)
                    elif import_name not in self.STD_LIBS:
                        imports.add(import_name)
                    elif import_name in TKINTER_LIBS:
                        extra.add("tkinter")

        return imports, extra, deps

    def _parse_std_libs(self) -> typing.Set[str]:
        if not len(self.STD_LIBS):
            self.STD_LIBS = stdlib_list.stdlib_list(PYTHON_VER_SHORT)
            logging.info(f"Parse std libs: total=[{len(self.STD_LIBS)}]")
