version = '0.0.1'

from .project import Project as project
from .targets import (Executable as executable, StaticLibrary as static_library, SharedLibrary as shared_library)
from .interpreter import Interpreter

from mesonbuild import environment, interpreter

environment.build_filename = 'nosem-build.py'
interpreter.Interpreter = Interpreter
