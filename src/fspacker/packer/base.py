from fspacker.common import BuildTarget


class BasePacker:
    def __init__(self, target: BuildTarget):
        self.target = target

    def pack(self):
        pass
