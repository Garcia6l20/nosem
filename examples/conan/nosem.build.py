from nosem import (project, executable, dependency, find_program, run_command, current_source_dir, current_build_dir, \
                   error, test)

project('conan', default_options=[
    f'build.pkg_config_path={current_build_dir()}'
])

conan = find_program('conan', required=False)
if not conan.found():
    print(f'conan not found, conan-demo skipped')
else:
    build_dir = current_build_dir()
    source_dir = current_source_dir()
    result = run_command(conan.path(), 'install', source_dir, '-if', build_dir)
    if result.returncode != 0:
        error(f'conan error: {result.stderr}')

    catch2 = dependency('catch2', required=True)
    demo = executable('conan-demo', 'demo.cpp', dependencies=catch2)
    test('conan-demo', demo)
