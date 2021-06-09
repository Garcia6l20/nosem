from nosem import project, executable, dependency, test

project('testlib_depends', 'cpp',
        default_options=[
            'cpp_std=c++latest'
        ])

demo = executable('testlib-depends-demo', 'main.cpp',
                  dependencies=[
                      dependency('testlib', fallback=[
                                 'testlib', 'testlib_dep'])
                  ])
test(demo.name(), demo)
