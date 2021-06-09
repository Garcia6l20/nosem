from nosem import library, declare_dependency, files

testlib = library('testlib', 'test.cpp', 'test.hpp')
testlib_dep = declare_dependency(link_with=testlib, include_directories=['.'])
