from nosem import project, subdir

project('testlib', 'cpp',
    default_options=[
        'cpp_std=c++latest'
    ])

subdir('testlib')
subdir('exe')
