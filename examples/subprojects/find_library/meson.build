project('find_library', 'cpp')

fmt = meson.get_compiler('cpp').find_library('fmt')
if not fmt.found()
    print('sipping fmt-demo (fmt not found)')
else
    executable('fmt-demo', 'fmt-demo.cpp', dependencies: fmt)
endif
