import os
import importlib.util

from mesonbuild import build, interpreter, interpreterbase, mesonlib, environment, mlog
from mesonbuild.mesonlib import MachineChoice


class WrapResolver(interpreter.interpreter.wrap.Resolver):
    """ Overloaded wrap.Resolver
    """

    def resolve(self, subp_name, method, subproject):
        intr = Interpreter.get()
        abs_dir = os.path.join(intr.source_root, subp_name)
        build_file = os.path.join(abs_dir, environment.build_filename)
        if os.path.exists(build_file):
            return subp_name
        super().resolve(subp_name, method, subproject)


interpreter.interpreter.wrap.Resolver = WrapResolver


def load_module(path):
    spec = importlib.util.spec_from_file_location("meson_user_build", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Interpreter(interpreter.Interpreter):
    """ Overloaded Interpreter

    Actualy not an Interpreter, it only loads the nosem-build.py.
    """

    _current = None
    _root = None

    def __init__(self, *args, **kwargs):
        self.parent = Interpreter._current
        Interpreter._current = self

        if Interpreter._root is None:
            Interpreter._root = self

        super().__init__(*args, **kwargs)

    @staticmethod
    def get():
        return Interpreter._current

    @staticmethod
    def root():
        return Interpreter._root

    def load_root_meson_file(self) -> None:
        pass

    def load_root_project(self) -> None:
        load_module(os.path.join(self.source_root, self.root_subdir, environment.build_filename))
        if self.parent:
            Interpreter._current = self.parent

    def sanity_check_ast(self) -> None:
        pass

    def parse_project(self):
        self.load_root_project()
        self.project_args_frozen = True

    def run(self) -> None:
        pass


import mesonbuild

# global override iterpreter
mesonbuild.interpreter.interpreter.Interpreter = Interpreter
