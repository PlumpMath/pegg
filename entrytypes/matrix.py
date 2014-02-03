from .entrytype import EntryType
from .tools import fstr

class __Matrix(EntryType):
    def __init__(self, parent, matrix, precision=None):
        super().__init__(parent=parent)
        self.__test_matrix(matrix)
        for m in matrix:
            self.__test_matrix(m)
        self._precision = precision
        self._matrix = matrix

    def get_content(self):
        return "\n".join([" ".join(map(lambda value: fstr(value, self._precision), m)) for m in self._matrix])

    def __test_matrix(self, test):
        length = {"Matrix3":3, "Matrix4":4}[self.__class__.__name__]
        if not len(test) == length:
            raise MatrixFormatError("Invalid format for {0!r}, should be like {1}".format(
                self.__class__.__name__,
                [[col for col in range(length)] for row in range(length)]))

class Matrix3(__Matrix):
    def __init__(self, parent, matrix, precision=None):
        super().__init__(parent=parent, matrix=matrix, precision=precision)


class Matrix4(__Matrix):
    def __init__(self, parent, matrix, precision=None):
        super().__init__(parent=parent, matrix=matrix, precision=precision)


class MixInMatrix:
    def set_matrix3(self, matrix, precision=None):
        if self.get_parent().__class__.__name__ != "Texture":
            raise AttributeError("Matrix3 is only allowed within a Texture Entry")
        self._entries["Matrix3"] = Matrix3(self, matrix, precision=precision)

    def set_matrix4(self, matrix, precision=None):
        self._entries["Matrix4"] = Matrix4(self, matrix, precision=precision)