from .entrytype import EntryType
from .tools import strname

class Ref(EntryType):
    def __init__(self, parent, ref):
        super().__init__(parent=parent)
        if not ref in self.vertexpools:
            raise KeyError("VertexPool {0!r} does not exist.".format(ref))
        self._ref = strname(ref)

    def get_content(self):
        return self._ref


class MixInRef:
    def set_ref(self, ref):
        self._entries["Ref"] = Ref(self, ref)
