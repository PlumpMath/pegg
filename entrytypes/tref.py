from .entrytype import EntryType
from .tools import strname

class TRef(EntryType):
    def __init__(self, parent, tref):
        if not tref in self.get_pegg(parent).textures:
            raise KeyError("Texture {0!r} does not exists.".format(tref))
        super().__init__(parent=parent)
        self._tref = strname(tref)
        
    def get_content(self):
        return self._tref


class MixInTRef:
    def append_tref(self, tref):
        """
        This refers to a named <Texture> entry given earlier.  It applies
        the given texture to the polygon.  This requires that all the
        polygon's vertices have been assigned texture coordinates.

        This attribute may be repeated multiple times to specify
        multitexture.  In this case, each named texture is applied to the
        polygon, in the order specified.
        """
        self._entries["TRef"].append(TRef(self, tref))