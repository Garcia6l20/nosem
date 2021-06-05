from nosem import library, declare_dependency

testlib = library('testlib', 'test.cpp')
testlib_dep = declare_dependency(link_with=testlib, include_directories=['.'])
