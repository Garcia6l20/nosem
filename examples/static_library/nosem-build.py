from nosem import project, executable, static_library

project('static_lib', 'cpp')

lib = static_library('static-lib', 'test.cpp', include_directories=['.'])

executable('static-lib-demo', 'main.cpp', link_with=[lib])
