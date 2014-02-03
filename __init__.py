"""
Pegg module

Can be used as an easy library to create egg files for Panda3d.
Written by Jeroen van der Heijden.

"""
from .entrytypes.entrytype import EntryType
from .entrytypes.comment import MixInComment
from .entrytypes.coordinatesystem import MixInCoordinateSystem
from .entrytypes.group import MixInGroup, MixInInstance
from .entrytypes.material import MixInMaterial
from .entrytypes.texture import MixInTexture
from .entrytypes.vertexpool import MixInVertexPool

__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))
__all__ = ["Pegg", "Cube"]




class Pegg(
        EntryType,
        MixInComment,
        MixInCoordinateSystem,
        MixInGroup,
        MixInInstance,
        MixInMaterial,
        MixInTexture,
        MixInVertexPool):
    def __init__(self):
        super().__init__()

class Cube(Pegg):
    def __init__(self, size=2):
        # Initialize superclass
        super().__init__()

        # Divide the size by two because we go from minus-size to size
        size /= 2

        # Add a group named "Cube"
        group = self.add_group("Cube")

        # Add a vertexpool named "Cube"
        vertexpool = group.add_vertexpool("Cube")

        # Add the vertices
        vertexpool.add_vertex(0, size, size, -size)
        vertexpool.add_vertex(1, size, -size, -size)
        vertexpool.add_vertex(2, -size, -size, -size)
        vertexpool.add_vertex(3, -size, size, -size)
        vertexpool.add_vertex(4, size, size, size)
        vertexpool.add_vertex(5, size, -size, size)
        vertexpool.add_vertex(6, -size, -size, size)
        vertexpool.add_vertex(7, -size, size, size)

        # Append the polygons
        group.append_polygon(0, 1, 2, 3, ref="Cube")
        group.append_polygon(4, 7, 6, 5, ref="Cube")
        group.append_polygon(0, 4, 5, 1, ref="Cube")
        group.append_polygon(1, 5, 6, 2, ref="Cube")
        group.append_polygon(2, 6, 7, 3, ref="Cube")
        group.append_polygon(4, 0, 3, 7, ref="Cube")

