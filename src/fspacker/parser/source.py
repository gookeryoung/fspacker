import logging
import pathlib
import typing

from fspacker.config import IGNORE_DIRS, GUI_LIBS

__all__ = ("SourceParser",)

from fspacker.parser.deps import pack_src_deps

from fspacker.parser.entry import pack_entry
from fspacker.parser.library import pack_library

from fspacker.parser.project import ProjectConfig

from fspacker.repo.library import LibraryInfo, fetch_libs_repo
from fspacker.repo.runtime import pack_runtime


class SourceParser:
    def __init__(self, directory: str, root: str):
        self.directory = pathlib.Path(directory)
        self.root = pathlib.Path(root)
        self.targets: typing.Dict[str, ProjectConfig] = {}
        self.target_contents: typing.Dict[str, str] = {}

        self._parse_func: typing.Optional[typing.Callable] = None

        toml_file = self.directory / "pyproject.toml"
        if toml_file.is_file():
            self._parse_func = self._parse_toml
        else:
            logging.info(f"项目文件夹[{self.directory}]中未找到pyproject.toml")
            self._parse_func = self._parse_raw

        self._parse_func()

    def pack(self):
        for name, target in self.targets.items():
            pack_runtime(target)
            pack_entry(target)
            pack_src_deps(target)
            pack_library(target)

    def _parse_toml(self):
        """通过 pyproject.toml 分析项目结构"""
        pass

    def _parse_raw(self):
        """通过包含 main 的 py 文件分析项目结构"""
        logging.info("通过py文件分析项目结构")

        entries = sorted(
            list(self.directory.iterdir()), key=lambda x: x.is_dir()
        )
        for entry in entries:
            if entry.is_dir() and entry.stem.lower() not in IGNORE_DIRS:
                self._parse_dir(entry)
                continue
            if entry.is_file() and entry.suffix in ".py":
                self._parse_py_file(entry)
                continue
            if not len(self.targets):
                logging.info(f"路径[{self.directory}]下未找到有效构建目标")

    def _parse_dir(self, entry: pathlib.Path):
        for k, content in self.target_contents.items():
            if entry.stem in content:
                self.targets[k].deps.append(entry)
                logging.info(f"增加目录[{entry.name}]到[{self.targets[k]}]")
                continue
        else:
            p = SourceParser(entry, self.root)
            if len(p.targets):
                logging.info(f"更新打包目标[{p.targets}]")
                self.targets.update(p.targets)

    def _parse_py_file(self, filepath: pathlib.Path):
        dep_src = []

        with open(filepath, "r", encoding="utf-8") as f:
            content = "".join(f.readlines())
            if "def main" in content or "__main__" in content:
                libs = self._parse_libs(content)
                lib_names = set([_.package_name.lower() for _ in libs])
                is_gui = lib_names.intersection(GUI_LIBS)
                self.targets[filepath.stem] = ProjectConfig(
                    src=filepath, deps=dep_src, libs=libs, is_gui=is_gui
                )
                logging.info(f"增加打包目标[{self.targets[filepath.stem]}]")
                self.target_contents[filepath.stem] = content

    @staticmethod
    def _parse_libs(content: str) -> typing.List[LibraryInfo]:
        """分析引用的库"""
        libs: typing.List[LibraryInfo] = []
        libs_repos = fetch_libs_repo()
        for k, v in libs_repos.items():
            expressions: typing.List[str] = [
                f"import {v.package_name}",
                f"from {v.package_name}",
            ]
            for exp in expressions:
                if exp in content and v.package_name not in [
                    x.package_name for x in libs
                ]:
                    libs.append(v)
        return libs
