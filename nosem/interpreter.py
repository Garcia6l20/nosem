import os
import importlib.util

from mesonbuild import build, interpreter, mesonlib, environment, mlog
from mesonbuild.mesonlib import MachineChoice

from .project import Project


def load_module(path):
    spec = importlib.util.spec_from_file_location("meson_user_build", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Interpreter(interpreter.Interpreter):
    def load_root_meson_file(self) -> None:
        pass

    def sanity_check_ast(self) -> None:
        pass

    def build_func_dict(self) -> None:
        pass

    def parse_project(self):
        root = Project.get_root()

        self.add_languages(root.proj_langs, True, MachineChoice.HOST)
        self.add_languages(root.proj_langs, False, MachineChoice.BUILD)

        self.set_backend()

        self.build.projects[self.subproject] = root.name

        mlog.log('Project name:', mlog.bold(root.name))
        mlog.log('Project version:', mlog.bold(root.version or 'undefined'))

        for target in root.targets:
            build_target = target(self.environment, self.subdir, self.subproject, MachineChoice.HOST)
            self.add_stdlib_info(build_target)
            self.add_target(target.name, build_target)
            self.project_args_frozen = True

    def run(self) -> None:
        pass
