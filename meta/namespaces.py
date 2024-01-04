import types


class SnapshotNamespace(types.SimpleNamespace):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ParameterNamespace(types.SimpleNamespace):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)