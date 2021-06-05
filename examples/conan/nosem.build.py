from nosem import project, executable, dependency, run_command, current_source_dir, current_build_dir, error, test

project('conan')

build_dir = current_build_dir()
source_dir = current_source_dir()
result = run_command('conan', 'install', source_dir, '-if', build_dir)
if result.returncode != 0:
    error(f'conan error: {result.stderr}')

catch2 = dependency('catch2', required=True, extra_path=build_dir)
demo = executable('conan-demo', 'demo.cpp', dependencies=catch2)
test('conan-demo', demo)
