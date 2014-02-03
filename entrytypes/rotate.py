from .entrytype import EntryType
from .tools import fstr

class Rotate(EntryType):
    def __init__(self, parent, degrees, *args, precision=None):
        super().__init__(parent=parent)
        values = list(args)
        values.insert(0, degrees)
        if len(values) > 4:
            raise ValueError("Too many values given: {0} (maximum=4)".format(len(values)))
        self._precision = precision
        self._values = values

    def get_content(self):
        return " ".join(map(lambda value: fstr(value, self._precision), self._values))


class MixInRotate:
    def set_rotate(self, degrees, *args, precision=None):
        #if self.get_parent().__class__.__name__ != "Texture":
        #    raise Matrix3NotAllowedError("Matrix3 is only allowed within a Texture Entry")
        self._entries["Rotate"] = Rotate(self, degrees, *args, precision=precision)
