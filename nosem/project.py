class Project:

    _root = None
    _current = None

    @staticmethod
    def get_root():
        return Project._root

    @staticmethod
    def get_current():
        return Project._current

    @staticmethod
    def add_target(target):
        target.project = Project._current
        Project._current.targets.append(target)

    def __init__(self, name, proj_langs, version=None):
        self.name = name
        self.version = version
        self.proj_langs = [proj_langs] if isinstance(proj_langs, str) else proj_langs
        if Project._root is None:
            Project._root = self
        Project._current = self

        self.targets = list()
