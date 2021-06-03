from .project import Project as project
from .targets import (Executable as executable, StaticLibrary as static_library, SharedLibrary as shared_library)
from .interpreter import Interpreter
from .main import main

from mesonbuild import environment, interpreter

environment.build_filename = 'build.py'
interpreter.Interpreter = Interpreter
