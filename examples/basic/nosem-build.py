from nosem import project, executable, static_library

project('basic', 'cpp')

basic = static_library('basic', 'test.cpp', include_directories=['.'])

executable('basic-demo', 'main.cpp', link_with=[basic])
