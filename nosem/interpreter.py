import os
import importlib.util

from mesonbuild import build, interpreter, interpreterbase, mesonlib, environment, mlog
from mesonbuild.interpreterbase import InterpreterException
from mesonbuild.mesonlib import MachineChoice


class WrapResolver(interpreter.interpreter.wrap.Resolver):
    """ Overloaded wrap.Resolver
    """

    def resolve(self, subp_name, method, subproject):
        intr = Interpreter.get()
        abs_dir = os.path.join(intr.source_root, self.subdir, subp_name)
        build_file = os.path.join(abs_dir, environment.build_filename)
        if os.path.exists(build_file):
            return os.path.join(self.subdir, subp_name)
        super().resolve(subp_name, method, subproject)


interpreter.interpreter.wrap.Resolver = WrapResolver


def get_interpreter_objects(module):
    from inspect import getmembers
    return {k: v for k, v in getmembers(module, lambda obj: hasattr(obj, 'holder'))}


class Interpreter(interpreter.Interpreter):
    """ Overloaded Interpreter

    Actualy not an Interpreter, it only loads the nosem-build.py.
    """

    _current = None
    _root = None

    def __init__(self, *args, **kwargs):

        self.root_module = None

        self.parent = Interpreter._current
        Interpreter._current = self

        if Interpreter._root is None:
            Interpreter._root = self

        super().__init__(*args, **kwargs)

    def load_module(self, path, is_root=False, **kwargs):
        spec = importlib.util.spec_from_file_location("meson_user_build", path)
        module = importlib.util.module_from_spec(spec)
        if is_root:
            self.root_module = module
        module.__dict__.update(**kwargs)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def get():
        return Interpreter._current

    @staticmethod
    def root():
        return Interpreter._root

    def load_root_meson_file(self) -> None:
        pass

    def load_root_project(self) -> None:
        self.load_module(os.path.join(self.source_root, self.root_subdir, environment.build_filename), is_root=True)
        if self.parent:
            Interpreter._current = self.parent

    def sanity_check_ast(self) -> None:
        pass

    def parse_project(self):
        self.load_root_project()
        self.project_args_frozen = True

    def run(self) -> None:
        pass

    def func_subdir(self, node, args, kwargs):
        self.validate_arguments(args, 1, [str])
        mesonlib.check_direntry_issues(args)
        if '..' in args[0]:
            raise InvalidArguments('Subdir contains ..')
        if self.subdir == '' and args[0] == self.subproject_dir:
            raise InvalidArguments('Must not go into subprojects dir with subdir(), use subproject() instead.')
        if self.subdir == '' and args[0].startswith('meson-'):
            raise InvalidArguments('The "meson-" prefix is reserved and cannot be used for top-level subdir().')
        for i in mesonlib.extract_as_list(kwargs, 'if_found'):
            if not hasattr(i, 'found_method'):
                raise InterpreterException('Object used in if_found does not have a found method.')
            if not i.found_method([], {}):
                return
        prev_subdir = self.subdir
        subdir = os.path.join(prev_subdir, args[0])
        if os.path.isabs(subdir):
            raise InvalidArguments('Subdir argument must be a relative path.')
        absdir = os.path.join(self.environment.get_source_dir(), subdir)
        symlinkless_dir = os.path.realpath(absdir)
        build_file = os.path.join(symlinkless_dir, 'meson.build')
        if build_file in self.processed_buildfiles:
            raise InvalidArguments('Tried to enter directory "%s", which has already been visited.'
                                   % subdir)
        self.processed_buildfiles.add(build_file)
        self.subdir = subdir
        os.makedirs(os.path.join(self.environment.build_dir, subdir), exist_ok=True)
        buildfilename = os.path.join(self.subdir, environment.build_filename)
        self.build_def_files.append(buildfilename)
        absname = os.path.join(self.environment.get_source_dir(), buildfilename)
        if not os.path.isfile(absname):
            self.subdir = prev_subdir
            raise InterpreterException(f"Non-existent build file '{buildfilename!s}'")

        module = self.load_module(absname, **get_interpreter_objects(self.root_module))
        self.root_module.__dict__.update(**get_interpreter_objects(module))
        self.subdir = prev_subdir
        return module

    def set_variable(self, varname: str, variable) -> None:
        if variable is None:
            raise InvalidCode('Can not assign None to variable.')
        self.variables[varname] = variable

    def make_test(self, node, args, kwargs):
        args[1] = args[1].holder
        return super().make_test(node, args, kwargs)


import mesonbuild

# global override iterpreter
mesonbuild.interpreter.interpreter.Interpreter = Interpreter
