project('conan', 'cpp',
        default_options: [
            'pkg_config_path=@0@'.format(meson.build_root())
        ])

conan = find_program('conan', required: false)
if not conan.found()
    print(f'conan not found, conan-demo skipped')
else
    result = run_command(conan.path(), 'install', meson.current_source_dir(), '-if', meson.build_root())
    if result.returncode() != 0
        error('conan error: @0@'.format(result.stderr()))
    endif
    catch2 = dependency('catch2', required: true)
    demo = executable('conan-demo', 'demo.cpp', dependencies: catch2)
    test('conan-demo', demo)
endif
