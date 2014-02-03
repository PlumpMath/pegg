from .entrytype import EntryType

class Scalar(EntryType):
    def __init__(self, parent, name, value):
        super().__init__(parent=parent, name=name)
        self._value = value

    def get_content(self):
        return str(self._value)

class MixInScalar:
    def add_scalar(self, name, value):
        self._entries["Scalar"][name] = Scalar(self, name, value)

    def get_scaler(self, name, default=None):
        return self._entries["Scalar"][name].get_content() if name in self._entries["Scalar"] else default;