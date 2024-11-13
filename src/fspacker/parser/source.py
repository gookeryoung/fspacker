import logging
import pathlib
import typing


__all__ = ("SourceParser",)

from fspacker.parser.base import BaseParser
from fspacker.repo.library import get_libs_std

import ast
from fspacker.common import BuildTarget


class SourceParser(BaseParser):
    """Parse by source code"""

    def parse(self, entry: pathlib.Path):
        with open(entry, encoding="utf-8") as f:
            content = "".join(f.readlines())
            if "def main" in content or "__main__" in content:
                ast_tree = self._parse_ast(content, entry)
                self.config.targets[entry.stem] = BuildTarget(
                    src=entry,
                    deps=set(),
                    ast=ast_tree,
                )
                logging.info(f"增加打包目标{self.config.targets[entry.stem]}")

    @staticmethod
    def _parse_ast(content: str, filepath: pathlib.Path) -> typing.Set[str]:
        """分析引用的库"""
        tree = ast.parse(content, filename=filepath)
        std_libs = get_libs_std()
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                import_name = node.module.split(".")[0]
                if import_name not in std_libs:
                    imports.add(import_name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    import_name = alias.name.split(".")[0]
                    if import_name not in std_libs:
                        imports.add(import_name)
        return imports
