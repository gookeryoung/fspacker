import logging
import pathlib
import typing


__all__ = ("SourceParser",)

import stdlib_list

from fspacker.config import PYTHON_VER_SHORT
from fspacker.parser.base import BaseParser

import ast
from fspacker.common import BuildTarget

__std_libs: typing.Set[str] = set()


class SourceParser(BaseParser):
    """Parse by source code"""

    def parse(self, entry: pathlib.Path):
        with open(entry, encoding="utf-8") as f:
            code = "".join(f.readlines())
            if "def main" in code or "__main__" in code:
                ast_tree, extra = self._parse_ast(code, entry)
                self.config.targets[entry.stem] = BuildTarget(
                    src=entry,
                    deps=set(),
                    ast=ast_tree,
                    extra=extra,
                    code=code,
                )
                logging.info(f"增加打包目标{self.config.targets[entry.stem]}")

    @staticmethod
    def _parse_ast(content: str, filepath: pathlib.Path) -> typing.Set[str]:
        """分析引用的库"""
        tree = ast.parse(content, filename=filepath)
        std_libs = _parse_std_libs()
        imports = set()
        extra = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                import_name = node.module.split(".")[0].lower()
                if import_name not in std_libs:
                    imports.add(import_name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    import_name = alias.name.split(".")[0].lower()
                    if import_name not in std_libs:
                        imports.add(import_name)
                    if import_name == "tkinter":
                        extra.add(import_name)
        return imports, extra


def _parse_std_libs() -> typing.Set[str]:
    global __std_libs

    if not len(__std_libs):
        __std_libs = stdlib_list.stdlib_list(PYTHON_VER_SHORT)
        logging.info(f"获取内置库[{len(__std_libs)}]个")
    return __std_libs
