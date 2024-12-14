import ast
import logging
import pathlib
import typing
from io import StringIO

from fspacker.config import TKINTER_LIBS
from fspacker.parser.base import BaseParser
from fspacker.parser.target import PackTarget
from fspacker.utils.repo import get_builtin_lib_repo

__all__ = ("SourceParser",)


class SourceParser(BaseParser):
    """Parse by source code"""

    def __init__(self, targets: typing.Dict[str, PackTarget], root_dir: pathlib.Path):
        super().__init__(targets, root_dir)

        self.entries: typing.Dict[str, pathlib.Path] = {}
        self.builtins = get_builtin_lib_repo()
        self.code_text = StringIO()

    def parse(self, entry: pathlib.Path):
        with open(entry, encoding="utf-8") as f:
            code = "".join(f.readlines())
            if "def main" in code or "__main__" in code:
                ast_tree, extra, deps = self._parse_ast(entry)
                self.targets[entry.stem] = PackTarget(
                    src=entry,
                    deps=deps,
                    ast=ast_tree,
                    extra=extra,
                    code=f"{code}{self.code_text.getvalue()}",
                )
                logging.info(f"Add pack target{self.targets[entry.stem]}")

    def _parse_ast(
        self, filepath: pathlib.Path
    ) -> typing.Tuple[typing.Set[str], typing.Set[str], typing.Set[str]]:
        """Analyse ast tree from source code"""
        with open(filepath, encoding="utf-8") as f:
            content = "".join(f.readlines())

        tree = ast.parse(content, filename=filepath)
        local_entries = {_.stem: _ for _ in filepath.parent.iterdir()}
        self.entries.update(local_entries)
        imports = set()
        extra = set()
        deps = set()

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
                    deps.add(import_name)
                    entry_file = local_entries.setdefault(import_name, None)

                    if entry_file:
                        if entry_file.is_file():
                            with open(entry_file, encoding="utf-8") as f:
                                self.code_text.write("".join(f.readlines()))
                        elif entry_file.is_dir():
                            files = list(_ for _ in entry_file.iterdir() if _.suffix == ".py")
                            for file in files:
                                vals = self._parse_ast(file)
                                imports |= vals[0]
                                extra |= vals[1]
                                deps |= vals[2]

                elif import_name not in self.builtins:
                    imports.add(import_name.lower())

                # import_name needs tkinter
                if import_name in TKINTER_LIBS:
                    extra.add("tkinter")

        return imports, extra, deps
