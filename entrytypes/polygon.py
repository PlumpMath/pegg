from .entrytype import EntryType
from .vertexref import MixInVertexRef
from .normal import MixInNormal
from .mref import MixInMRef
from .tref import MixInTRef

class Polygon(EntryType, MixInVertexRef, MixInNormal, MixInMRef, MixInTRef):
    def __init__(self, parent, *vertices, ref):
        super().__init__(parent=parent)
        self.append_vertexref(*vertices, ref=ref)

class MixInPolygon:
    def append_polygon(self, *vertices, ref):
        polygon = Polygon(self, *vertices, ref=ref)
        self._entries["Polygon"].append(polygon)
        return polygon

    @property
    def polygons(self):
        return tuple(self._entries["Polygon"])



