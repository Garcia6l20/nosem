from nosem import project, subproject, current_build_dir

project('nosem-examples', 'cpp',
        default_options=[
            f'pkg_config_path={current_build_dir()}'
        ])

subproject('basic')
subproject('static_library')
subproject('find_library')
subproject('conan')
