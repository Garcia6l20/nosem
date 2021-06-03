# *Nosem* build system

*Nosem* is tiny overlay to *Meson*.

While you call meson to interpret you *meson.build* file,
with nosem you directly invoke your *build.py*.

This inverted process removes many limitations from meson
and you are free to use any python library directly.

The whole scripting part of meson is bypassed

### Meson

```meson
project('myproj', 'cpp')
executable('example', 'main.cpp')
```

```
meson build
cd build && ninja
```

### Nosem

```python
#!/usr/bin/env python
from nosem import project, executable, main

project('myproj', 'cpp')
executable('example', 'main.cpp')

main()
```
```
./build.py build
cd build && ninja
```
