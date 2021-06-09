from nosem import project, executable, test

project('basic', 'cpp')
demo = executable('basic-demo', 'main.cpp')
test(demo.name(), demo)
