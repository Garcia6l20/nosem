project('conan', 'cpp',
        default_options: [
            'pkg_config_path=@0@'.format(meson.current_build_dir())
        ])

conan = find_program('conan', required: false)
if not conan.found()
    print(f'conan not found, conan-demo skipped')
else
    build_dir = meson.current_build_dir()
    source_dir = meson.current_source_dir()
    result = run_command(conan.path(), 'install', source_dir, '-if', build_dir)
    if result.returncode() != 0
        error('conan error: @0@'.format(result.stderr()))
    endif
    catch2 = dependency('catch2', required: true)
    demo = executable('conan-demo', 'demo.cpp', dependencies: catch2)
    test('conan-demo', demo)
endif
