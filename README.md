# FSPacker

Fast & Simple Packer toolset for python.

## Key Features

- [x] 10-100x faster than existing deploy libs such as Py2exe, PyInstaller, Nuitka...
- [x] Supports multi-project deployment
- [x] Supports offline packing
- [ ] Supports archiving with zip or 7z
- [ ] Supports deployment with InnoSetup
- [ ] Supports compilation with nuitka
- [ ] Supports encryption with PyArmor

## Support Platforms

- [x] Windows 7 ~ 11
- [ ] linux
- [ ] macOS

## Support Libraries

- [x] tkinter(Windows only)
- [x] pyside2
- [x] matplotlib
- [x] pandas
- [x] pytorch

## Quick Start

Usage:

```bash
pip install fspacker
cd [directory/of/app.py]
fsp
```

> **!!!NOTICE!!!**
> 'app.py' must contain 'main' function as entry.

Example:

Python project structure:

```bash
ex01_helloworld_console/
|___ modules/
    |____ __init__.py
    |____ module_a.py
    |____ module_b.py
|___ ex01_helloworld_console.py
|___ module_c.py

```

```python
# ex01_helloworld_console.py
from modules.module_a import function_a  # import from
from modules.module_b import function_b  # import from
import module_c  # import


def main():
    print("hello, world")

    function_a()
    function_b()
    module_c.function_c()
```

Run command:

```bash
cd .../ex01_helloworld_console
fsp
```
