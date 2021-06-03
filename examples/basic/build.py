#!/usr/bin/env python

from nosem import project, executable, static_library, main

project('basic', 'cpp')

basic = static_library('basic', 'test.cpp', include_directories=['.'])

executable('basic-demo', 'main.cpp', link_with=[basic])

if __name__ == '__main__':
    main()
