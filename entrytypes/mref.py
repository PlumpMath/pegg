from .entrytype import EntryType
from .tools import strname

class MRef(EntryType):
    def __init__(self, parent, mref):
        if not mref in self.get_pegg(parent).materials:
            raise KeyError("Material {0!r} does not exists.".format(mref))
        super().__init__(parent=parent)
        self._mref = strname(mref)
        
    def get_content(self):
        return self._mref

class MixInMRef:
    def set_mref(self, mref):
        self._entries["MRef"] = MRef(self, mref)