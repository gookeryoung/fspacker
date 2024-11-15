from fspacker.packer.libspec.base import LibSpecPackerMixin


class PySide2Packer(LibSpecPackerMixin):
    PATTERNS = dict(
        pyside2={
            "PySide2/__init__.py",
            "PySide2/pyside2.abi3.dll",
            "PySide2/Qt5?Core",
            "PySide2/Qt5?Gui",
            "PySide2/Qt5?Widgets",
            "PySide2/Qt5?Network.dll",
            "PySide2/Qt5?Network.py.*",
            "PySide2/Qt5?Qml.dll",
            "PySide2/Qt5?Qml.py.*",
            "plugins/iconengines/qsvgicon.dll",
            "plugins/imageformats/.*.dll",
            "plugins/platforms/.*.dll",
        },
        shiboken2={},
        six={},
    )
