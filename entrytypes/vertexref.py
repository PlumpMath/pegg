from .entrytype import EntryType
from .ref import MixInRef

class VertexRef(EntryType, MixInRef):
    def __init__(self, parent, *vertices, ref):
        super().__init__(parent=parent)
        self.set_ref(ref)
        for vertex in vertices:
            if not vertex in self.vertexpools[ref]._entries["Vertex"]:
                raise KeyError("Vertex {0} not found in VertexPool {1!r}".format(vertex, ref))
        self._vertices = vertices

    def get_content(self):
        return " ".join(map(str, self._vertices))


class MixInVertexRef:
    def append_vertexref(self, *vertices, ref):
        self._entries["VertexRef"].append(VertexRef(self, *vertices, ref=ref))