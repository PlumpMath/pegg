from .entrytype import EntryType
from .matrix import MixInMatrix
from .rotate import MixInRotate

class Transform(EntryType, MixInMatrix, MixInRotate):
    def __init__(self, parent):
        super().__init__(parent=parent)

class MixInTransform:
    """
    This MixIn is used for the Texture and Group entry-types"
    """
    @property
    def transform(self):
        if self._entries["Transform"] is None:
            self._entries["Transform"] = Transform(self)
        return self._entries["Transform"]
