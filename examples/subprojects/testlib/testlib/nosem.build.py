from nosem import static_library, declare_dependency

testlib = static_library('testlib', 'test.cpp', 'test.hpp')
testlib_dep = declare_dependency(link_with=testlib, include_directories=['.'])
