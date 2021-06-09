project('testlib_depends', 'cpp',
        default_options: [
            'cpp_std=c++latest'
        ])

executable('testlib-depends-demo', 'main.cpp',
    dependencies:[
        dependency('testlib', fallback: ['testlib', 'testlib_dep'])
    ])
