from .project import Project

from mesonbuild import build, dependencies
from mesonbuild.mesonlib import File


class BaseTaget:

    def __init__(self, name, sources, dependencies=None, include_directories=None, install_mode=None, objects=None,
                 extra_files=None, link_with=None):
        self.name = name
        self.sources = [sources] if isinstance(sources, str) else sources
        self.objects = objects or list()
        self.link_with = link_with or list()
        self.dependencies = dependencies or list()
        self.include_directories = include_directories or list()
        Project.add_target(self)
        self.meson_target = None

    def __call__(self, env, subdir, subproject, for_machine, **kwargs):

        def to_meson(param, transform):
            value = getattr(self, param)
            if isinstance(value, list):
                if len(value):
                    kwargs[param] = [transform(item) for item in value]
            else:
                raise NotImplemented()

        to_meson('link_with', lambda lib: lib.meson_target)
        to_meson('dependencies', lambda dep: dependencies.Dependency(dep.meson_target, dict()))

        # kwargs['include_directories'] = self.include_directories
        self.meson_target = self.get_build_class()(self.name, subdir, subproject, for_machine,
                                      [File(False, subdir, s) for s in self.sources], self.objects, env, kwargs)
        return self.meson_target

    def get_build_class(self):
        raise NotImplementedError('get_build_class')


class Executable(BaseTaget):

    def get_build_class(self):
        return build.Executable


class StaticLibrary(BaseTaget):

    def get_build_class(self):
        return build.StaticLibrary


class SharedLibrary(BaseTaget):

    def get_build_class(self):
        return build.SharedLibrary
