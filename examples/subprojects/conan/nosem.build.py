from nosem import (project, executable, dependency, find_program, run_command, current_source_dir, build_root, \
                   error, test)

project('conan', 'cpp', default_options=[
    f'pkg_config_path={build_root()}'
])

conan = find_program('conan', required=False)
if not conan.found():
    print(f'conan not found, conan-demo skipped')
else:
    result = run_command(conan.path(), 'install', current_source_dir(), '-if', build_root())
    if result.returncode != 0:
        error(f'conan error: {result.stderr}')

    catch2 = dependency('catch2', required=True)
    demo = executable('conan-demo', 'demo.cpp', dependencies=catch2)
    test('conan-demo', demo)
