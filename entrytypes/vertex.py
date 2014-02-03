from .entrytype import EntryType
from .uv import MixInUV
from .normal import MixInNormal
from .tools import fstr, ProtectedDict

class Vertex(EntryType, MixInUV, MixInNormal):
    def __init__(self, parent, number, x, *coordinates, precision=None): # coordinates y, z, and w are optional
        super().__init__(parent=parent, name=number)
        self._precision = precision
        self._coordinates = list(coordinates)
        self._coordinates.insert(0, x)
        if len(self._coordinates) > 4:
            raise ValueError("Too many coordinate values given: {0} (maximum=4)".format(len(self._coordinates)))

    def get_content(self):
        return " ".join(map(lambda value: fstr(value, self._precision), self._coordinates))

    @property
    def x(self):
        return self.__get_coordinate(0)

    @property
    def y(self):
        return self.__get_coordinate(1)

    @property
    def z(self):
        return self.__get_coordinate(2)

    @property
    def w(self):
        return self.__get_coordinate(3)

    def __get_coordinate(self, num):
        try:
            return self._coordinates[num]
        except IndexError:
            return None

class MixInVertex:
    def add_vertex(self, number, x, *coordinates, precision=None):
        """
        <Vertex> number { x [y [z [w]]] [attributes] }

        A <Vertex> entry is only valid within a vertex pool definition.
        The number is the index by which this vertex will be referenced.
        It is optional; if it is omitted, the vertices are implicitly
        numbered consecutively beginning at one.  If the number is
        supplied, the vertices need not be consecutive.

        Normally, vertices are three-dimensional (with coordinates x, y,
        and z); however, in certain cases vertices may have fewer or more
        dimensions, up to four.  This is particularly true of vertices
        used as control vertices of NURBS curves and surfaces.  If more
        coordinates are supplied than needed, the extra coordinates are
        ignored; if fewer are supplied than needed, the missing
        coordinates are assumed to be 0.

        The vertex's coordinates are always given in world space,
        regardless of any transforms before the vertex pool or before the
        referencing geometry.  If the vertex is referenced by geometry
        under a transform, the egg loader will do an inverse transform to
        move the vertex into the proper coordinate space without changing
        its position in world space.  One exception is geometry under an
        <Instance> node; in this case the vertex coordinates are given in
        the space of the <Instance> node.  (Another exception is a
        <DynamicVertexPool>; see below.)

        In neither case does it make a difference whether the vertex pool
        is itself declared under a transform or an <Instance> node.  The
        only deciding factor is whether the geometry that *uses* the
        vertex pool appears under an <Instance> node.  It is possible for
        a single vertex to be interpreted in different coordinate spaces
        by different polygons.
        """
        if type(number) is not int:
            raise TypeError("number should be a type int, not {0}".format(type(number)))
        if number in self._entries["Vertex"]:
            raise ValueError("Cannot add {0!r}, the vertex number already exists.".format(number))
        vertex = self._entries["Vertex"][number] = Vertex(self, number, x, *coordinates, precision=precision)
        return vertex

    @property
    def vertices(self):
        return ProtectedDict(self._entries["Vertex"])