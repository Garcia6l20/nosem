from nosem import project, executable, test, get_compiler

project('find_library')

fmt = get_compiler('cpp').find_library('fmt', required=False)
if not fmt.found():
    print('sipping fmt-demo (fmt not found)')
else:
    demo = executable('fmt-demo', 'fmt-demo.cpp', dependencies=fmt)
    test('fmt-demo', demo)
