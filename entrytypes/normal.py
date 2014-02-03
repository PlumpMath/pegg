from .entrytype import EntryType
from .tools import fstr

class Normal(EntryType):
    def __init__(self, parent, *vector, precision=None): # vector x, y, z

        super().__init__(parent=parent)
        self._precision = precision
        self._vector = vector
        if len(self._vector) != 3:
            raise ValueError("A vector needs 3 values for x, y and z. {0} values are given".format(len(self._vector)))

    def __repr__(self):
        return self._vector

    def get_content(self):
        return " ".join(map(lambda value: fstr(value, self._precision), self._vector))


class MixInNormal:
    def set_normal(self, *vector, precision=None):
        """
        <Normal> { x y z [morph-list] }

        This specifies the surface normal of the vertex.  If omitted, the
        vertex will have no normal.  Normals may also be morphed;
        morph-list here is thus an optional list of <DNormal> entries,
        similar to the above.
        """
        normal = self._entries["Normal"] = Normal(self, *vector, precision=precision)
        return normal

    def get_normal(self):
        return self._entries["Normal"]