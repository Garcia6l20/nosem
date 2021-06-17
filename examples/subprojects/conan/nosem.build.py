from nosem import (project, executable, dependency, find_program, run_command, current_source_dir, build_root, \
                   error, test)
import platform

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

    # workaround: no way to make pkg-config work on Windows...
    # and conan's find package is TitleCase
    catch2_name = 'catch2'
    catch2_extra_args = dict()
    if platform.system() == 'Windows':
        catch2_name = catch2_name.title()
        catch2_extra_args = {
            'cmake_module_path': build_root()
        }

    catch2 = dependency(catch2_name, required=True, **catch2_extra_args)
    demo = executable('conan-demo', 'demo.cpp', dependencies=catch2)
    test(demo.name(), demo)
