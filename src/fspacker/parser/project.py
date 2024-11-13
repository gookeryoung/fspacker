import dataclasses
import pathlib
import typing


__all__ = ("ProjectConfig",)


@dataclasses.dataclass
class ProjectConfig:
    src: pathlib.Path
    is_gui: bool
    deps: typing.List[pathlib.Path]
    libs: typing.Set[str]

    def __repr__(self):
        deps = [_.stem for _ in self.deps]
        return f"src={self.src}, deps={deps}, libs={self.libs}"
