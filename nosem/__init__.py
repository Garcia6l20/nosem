version = '0.0.1'

from .interpreter import Interpreter

from mesonbuild import environment, interpreter
import functools

environment.build_filename = 'nosem-build.py'
interpreter.Interpreter = Interpreter


def __create_unwrapped_funcs():
    # list of functions available to nosem-build.py
    funcs = ['add_global_arguments',
             'add_project_arguments',
             'add_global_link_arguments',
             'add_project_link_arguments',
             'add_test_setup',
             'add_languages',
             'alias_target',
             'assert',
             'benchmark',
             'build_target',
             'configuration_data',
             'configure_file',
             'custom_target',
             'declare_dependency',
             'dependency',
             'disabler',
             'environment',
             'error',
             'executable',
             'generator',
             'gettext',
             'get_option',
             'get_variable',
             'files',
             'find_library',
             'find_program',
             'include_directories',
             'import',
             'install_data',
             'install_headers',
             'install_man',
             'install_subdir',
             'is_disabler',
             'is_variable',
             'jar',
             'join_paths',
             'library',
             'message',
             'project',
             'warning',
             'option',
             'run_target',
             'run_command',
             'set_variable',
             'subdir',
             'subproject',
             'summary',
             'shared_library',
             'shared_module',
             'static_library',
             'both_libraries',
             'test',
             'vcs_tag']
    for func_name in funcs:
        def unwrapped(fname, *args, **kwargs):
            func = Interpreter.get().funcs[fname]
            return func(None, list(args), kwargs)

        globals()[func_name] = functools.partial(unwrapped, func_name)


__create_unwrapped_funcs()


def with_meson(func):
    def wrapper(*args, **kwargs):
        meson = Interpreter.get().builtin['meson']
        return func(meson, *args, **kwargs)
    return wrapper

def meson_method(name):
    class FakeState:
        current_node = None
        subproject = None
    @with_meson
    def wrapper(meson, name, *args, **kwargs):
        method = meson.methods[name]
        class Wrapper:
            holder = method(list(args), kwargs)
            def __getattribute__(self, item):
                if item in Wrapper.holder.methods:
                    def wrapper(*args, **kwargs):
                        FakeState.subproject = Interpreter.get()
                        return Wrapper.holder.methods[item](list(args), kwargs)
                    return wrapper
                else:
                    return getattr(Wrapper.holder, item)
        return Wrapper()
    return functools.partial(wrapper, name)

def __getattr__(name):
    return meson_method(name)
