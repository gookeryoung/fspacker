import ast
import logging
import pathlib
import typing

from fspacker.common import PackTarget
from fspacker.config import TKINTER_LIBS
from fspacker.parser.base import BaseParser
from fspacker.utils.repo import get_builtin_lib_repo

__all__ = ("SourceParser",)


class SourceParser(BaseParser):
    """Parse by source code"""

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

    @staticmethod
    def _parse_ast(content: str, filepath: pathlib.Path) -> typing.Tuple[typing.Set[str], ...]:
        """Analyse ast tree from source code"""

        builtins = get_builtin_lib_repo()
        tree = ast.parse(content, filename=filepath)
        entries = list(_.stem for _ in filepath.parent.iterdir())
        imports = set()
        extra = set()
        deps = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module is not None:
                    import_name = node.module.split(".")[0].lower()

                    # import from local files or package folders
                    if import_name in entries:
                        deps.add(import_name)
                    # imports ast
                    elif import_name not in builtins:
                        imports.add(import_name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    import_name = alias.name.split(".")[0].lower()
                    if import_name in entries:
                        deps.add(import_name)
                    elif import_name not in builtins:
                        imports.add(import_name)

                    if import_name in TKINTER_LIBS:
                        extra.add("tkinter")

        return imports, extra, deps
