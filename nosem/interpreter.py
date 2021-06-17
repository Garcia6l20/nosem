import os
import importlib.util
from re import sub

from mesonbuild import build, interpreter, interpreterbase, mesonlib, environment, mlog
from mesonbuild.interpreterbase import InterpreterException, InvalidArguments, InvalidCode
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
    wrapped_objects = {k: v for k, v in getmembers(module, lambda obj: hasattr(obj, 'holder'))}
    return wrapped_objects


class Interpreter(interpreter.Interpreter):
    """ Overloaded Interpreter

    Actualy not an Interpreter, it only loads the nosem-build.py.
    """

    _current = None
    _root = None
    _rootModule = None
    _module_num = 0

    def __init__(self, *args, **kwargs):

        self.root_module = None
        self.subdir_module = None
        self.module = None

        self.parent = Interpreter._current
        Interpreter._current = self

        if Interpreter._root is None:
            Interpreter._root = self

        super().__init__(*args, **kwargs)

    def get_subproject(self, subp_name):
        subprojects = Interpreter._root.subprojects
        self.subprojects = subprojects
        return subprojects[subp_name] if subp_name in subprojects else None


    # def get_variable_method(self, args, kwargs):
    #     varname = args[0]
    #     mod_dict = self.module.__dict__
    #     return mod_dict[varname] if varname in mod_dict else None

    # def get_subproject_dep(self, name, display_name, subp_name, varname, kwargs):


    def load_module(self, path, is_root=False, **kwargs):
        spec = importlib.util.spec_from_file_location("meson_user_build_" + str(Interpreter._module_num), path)
        Interpreter._module_num += 1
        self.module = importlib.util.module_from_spec(spec)
        if is_root:
            self.root_module = self.module
            if not Interpreter._rootModule:
                Interpreter._rootModule = self.module
        else:
            self.subdir_module = self.module
        self.module.__dict__.update(**kwargs)
        for name, wrapper in kwargs.items():
            self.variables[name] = wrapper.holder
        spec.loader.exec_module(self.module)
        return self.module

    @staticmethod
    def get():
        return Interpreter._current

    @staticmethod
    def root():
        return Interpreter._root

    def load_root_meson_file(self) -> None:
        pass

    def load_root_project(self) -> None:
        absname = os.path.join(self.source_root, self.root_subdir, environment.build_filename)
        objects = dict()
        if self.parent:
            objects = get_interpreter_objects(self.parent.root_module)
        module = self.load_module(absname, is_root=True, **objects)
        if self.parent:
            Interpreter._current = self.parent
            self.parent.root_module.__dict__.update(**get_interpreter_objects(module))
        return module

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

        prev_module = self.subdir_module
        interpreter_objs = get_interpreter_objects(self.root_module)
        if self.subdir_module:
            interpreter_objs.update(**get_interpreter_objects(self.subdir_module))
        module = self.load_module(absname, **interpreter_objs)
        objects = get_interpreter_objects(module)
        if self.subdir_module:
            self.subdir_module.__dict__.update(**objects)
        self.root_module.__dict__.update(**objects)
        for name, wrapper in objects.items():
            self.variables[name] = wrapper.holder
        self.subdir = prev_subdir
        self.subdir_module = prev_module
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

import mesonbuild.mintro

from pathlib import Path

# build.meson hard coded in mintro
original_list_targets = mesonbuild.mintro.list_targets
def list_targets(*args, **kwargs):
    tlist = original_list_targets(*args, **kwargs)
    for t in tlist:
        p = Path(t['defined_in'])
        t['defined_in'] = str(p.parent / environment.build_filename)
    return tlist
mesonbuild.mintro.list_targets = list_targets
