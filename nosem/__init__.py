version = '0.0.2'

from .interpreter import Interpreter

from mesonbuild import environment, interpreter, interpreterbase
import functools
from pathlib import Path

environment.build_filename = 'nosem.build.py'
interpreter.Interpreter = Interpreter

class Wrapper:
    def __init__(self, holder):
        self.holder = holder

    def __getattr__(self, item):
        if hasattr(self.holder, item):
            return getattr(self.holder, item)
        elif item in self.holder.methods:
            def wrapper(*args, **kwargs):
                return self.holder.methods[item](list(args), kwargs)
            return wrapper
        else:
            raise ValueError()

def _unwrap_result(result):
    if not isinstance(result, interpreterbase.InterpreterObject):
        return result
    else:
        return Wrapper(result)


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
             'subdir_done',
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
            return _unwrap_result(func(None, list(args), kwargs))

        globals()[func_name] = functools.partial(unwrapped, func_name)


__create_unwrapped_funcs()


def with_meson(func):
    def wrapper(*args, **kwargs):
        meson = Interpreter.get().builtin['meson']
        return func(meson, *args, **kwargs)

    return wrapper


def meson_method(name):
    @with_meson
    def wrapper(meson, name, *args, **kwargs):
        method = meson.methods[name]
        return _unwrap_result(method(list(args), kwargs))

    return functools.partial(wrapper, name)

def import_module(filename, **kwargs):
    import importlib
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(filename)
    spec = importlib.util.spec_from_file_location(path.stem, path.as_posix())


    module = importlib.util.module_from_spec(spec)
    module.__dict__.update(**kwargs)
    spec.loader.exec_module(module)
    return Wrapper(module)

def __getattr__(name):
    return meson_method(name)
