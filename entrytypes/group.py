from .entrytype import EntryType
from .transform import MixInTransform
from .vertexpool import MixInVertexPool
from .polygon import MixInPolygon
from .tools import ProtectedDict

class MixInGroup:
    def add_group(self, name):
        """
        <Group> name { group-body }

        A <Group> node is the primary means of providing structure to the
        egg file.  Groups can contain vertex pools and polygons, as well as
        other groups.  The egg loader translates <Group> nodes directly into
        PandaNodes in the scene graph (although the egg loader reserves the
        right to arbitrarily remove nodes that it deems unimportant--see the
        <Model> flag, below to avoid this).  In addition, the following
        entries can be given specifically within a <Group> node to specify
        """
        if name in self._entries["Group"]:
            raise ValueError("Cannot add {0!r}, the group already exists.".format(name))
        group = self._entries["Group"][name] = Group(self, name)
        return group

    @property
    def groups(self):
        return ProtectedDict(self._entries["Group"])

class MixInInstance:
    def add_instance(self, name):
        """
        <Instance> name { instance-body }

        An <Instance> node is exactly like a <Group> node, except that
        vertices referenced by geometry created under the <Instance> node
        are not assumed to be given in world coordinates, but are instead
        given in the local space of the <Instance> node itself (including
        any transforms given to the node).

        In other words, geometry under an <Instance> node is defined in
        local coordinates.  In principle, similar geometry can be created
        under several different <Instance> nodes, and thus can be positioned
        in a different place in the scene each instance.  This doesn't
        necessarily imply the use of shared geometry in the Panda3D scene
        graph, but see the <Ref> syntax, below.
        """
        if name in self._entries["Instance"]:
            raise ValueError("Cannot add {0!r}, the instance already exists.".format(name))
        instance = self._entries["Instance"][name] = Instance(self, name)
        return instance

    @property
    def instances(self):
        return ProtectedDict(self._entries["Instance"])

class Group(EntryType, MixInGroup, MixInInstance, MixInTransform, MixInVertexPool, MixInPolygon):
    def __init__(self, parent, name):
        super().__init__(parent=parent, name=name)

class Instance(Group):
    def __init__(self, parent, name):
        super().__init__(parent=parent, name=name)



