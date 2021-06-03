# *Nosem* build system

*Nosem* is tiny overlay to *Meson*.

While you call meson to interpret you *meson.build* file,
with nosem you directly invoke your *build.py*.

This inverted process removes many limitations from meson
and you are free to use any python library directly.

The whole scripting part of meson is bypassed

### Meson

meson.build:
```meson
project('myproj', 'cpp')
executable('example', 'main.cpp')
```

```
meson build
cd build && ninja
```

### Nosem

nosem-build.py:
```python
from nosem import project, executable

project('myproj', 'cpp')
executable('example', 'main.cpp')
```

```
nosem build
cd build && ninja
```

## API

The API is exactly the same as meson available [here](https://mesonbuild.com/Reference-manual.html).
It defers only in the syntax, *nosem-build.py* file are pure python.

## How it works

The *meson.build* script interpretation is bypassed, simply replaced by a python module loading.
