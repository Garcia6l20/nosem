from nosem import executable, test

demo = executable('testlib-demo', 'main.cpp', dependencies=[testlib_dep])
test(demo.name(), demo)
