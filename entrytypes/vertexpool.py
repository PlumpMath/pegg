from .entrytype import EntryType
from .vertex import MixInVertex

class VertexPool(EntryType, MixInVertex):
    def __init__(self, parent, name):
        super().__init__(parent=parent, name=name)


class MixInVertexPool:
    def add_vertexpool(self, name):
        """
        <VertexPool> name { vertices }

        A vertex pool is a set of vertices.  All geometry is created by
        referring to vertices by number in a particular vertex pool.  There
        may be one or several vertex pools in an egg file, but all vertices
        that make up a single polygon must come from the same vertex pool.
        """
        if name in self.vertexpools:
            raise ValueError("Cannot add {0!r}, the vertexpool already exists within this pegg instance.".format(name))
        vertexpool = self._entries["VertexPool"][name] = VertexPool(self, name)
        return vertexpool
  
    # Property vertexpools is assign to EntryType to support this property on all subclasses