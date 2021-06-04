from nosem import project, executable, get_compiler

project('find_library')

fmt = get_compiler('cpp').find_library('fmt')
if not fmt.found():
    print('sipping fmt-demo (fmt not found)')
else:
    executable('fmt-demo', 'fmt-demo.cpp', dependencies=fmt)
