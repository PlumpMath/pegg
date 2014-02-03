from .entrytype import EntryType

class CoordinateSystem(EntryType):
    def __init__(self, parent, coordinatesystem):
        coordinatesystems = ["Y-up", "Z-up", "Y-up-right", "Z-up-right", "Y-up-left", "Z-up-left"]
        if coordinatesystem not in coordinatesystems:
            raise ValueError("Unknown CoordinateSystem {0!r}, should be: {1}".format(coordinatesystem, ", ".join(coordinatesystems)))
        super().__init__(parent=parent)
        self._coordinatesystem = coordinatesystem

    def get_content(self):
        return self._coordinatesystem

class MixInCoordinateSystem:
    def set_coordinatesystem(self, coordinatesystem="Y-up"):
        """
        <CoordinateSystem> { string }

        This entry indicates the coordinate system used in the egg file; the
        egg loader will automatically make a conversion if necessary.  The
        following strings are valid: Y-up, Z-up, Y-up-right, Z-up-right,
        Y-up-left, or Z-up-left.  (Y-up is the same as Y-up-right, and Z-up
        is the same as Z-up-right.)

        By convention, this entry should only appear at the beginning of the
        file, although it is technically allowed anywhere.  It is an error
        to include more than one coordinate system entry in the same file.
        If it is omitted, Y-up is assumed.
        """
        self._entries["CoordinateSystem"] = CoordinateSystem(self, coordinatesystem)

    def get_coordinatesystem(self):
        """
        Returns the coordinate system which can be set with the set_coordinatesystem() method.
        When the coordinate system is not set, the default 'Y-up' coordinate system will be returned.
        """
        coordinatesystem = self._entries["CoordinateSystem"].get_content()
        return "Y-up" if coordinatesystem is None else coordinatesystem