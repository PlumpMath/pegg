from .tools import strname, ProtectedDict

class EntryType:
    def __init__(self, parent=None, name=None):
        self._parent = parent
        self._name = None if name is None else strname(name) # We want this to be safe string, except for None
        self._entries = dict(
            Comment=list(),
            CoordinateSystem=None,
            Group=dict(),
            Instance=dict(),
            Material=dict(),
            Matrix3=None,
            Matrix4=None,
            MRef=None,
            Normal=None,
            Polygon=list(),
            Ref=None,
            Rotate=None,
            Scalar=dict(),
            Texture=dict(),
            Transform=None,
            TRef=list(),
            UV=dict(),
            Vertex=dict(),
            VertexPool=dict(),
            VertexRef=list(),
        )

    def __repr__(self):
        return "<{0}>".format(self.__class__.__name__) if self._name is None else "<{0} name={1!r}>".format(self.__class__.__name__, self._name)

    @property
    def vertexpools(self):
        """
        Returns a dictionary with all VertexPools within the total pegg instance.
        """
        vertexpools = {}
        def search_pegg(entry):
            vertexpools.update(entry._entries["VertexPool"])
            for group in list(entry._entries["Instance"].values()) + list(entry._entries["Group"].values()):
                search_pegg(group)
        search_pegg(self.get_pegg())
        return ProtectedDict(vertexpools)

    def _get(self, key, **kwargs):
        """
        Returns a string for the Entry/Entries for the given key.
        This method can handle dict, list and a single EntryType.
        """
        value = self._entries[key]
        entries = value if isinstance(value, list) else self._sorted(value) if isinstance(value, dict) else (value, ) if value is not None else ""
        return "".join([entry._prettify(**kwargs) for entry in entries])

    @staticmethod
    def _sorted(dictionary):
        """
        Returns a list with the values in the given dictionary ordered by the .keys()
        A None value in the dictionary will be the first list item and strings
        are sorted case-insensitive.
        """
        d = dictionary.copy()
        case_insensitive = lambda k: str.lower(k) if isinstance(k, str) else k
        nonevalue = d.pop(None) if None in d else None
        values = [d[key] for key in sorted(d.keys(), key=case_insensitive)]
        if nonevalue:
            values.insert(0, nonevalue)
        return values

    def get_content(self): # maybe use the @abc.abstractmethod decorator to enforce implementation of this method
        """
        Get the content of the EntryType. This method should be overwritten by subclasses when content is needed.
        """
        return None

    def get_scalar(self, name):
        """
        Returns the content of the given scalar, None if the scalar is not found.
        """
        return self._entries["Scalar"][name].get_content() if name in self._entries["Scalar"] else None

    def get_childs(self):
        """
        Returns a list of all EntryTypes which are childs from this instance.
        Note: this method is not recursive, sub-childs are not included.
        """
        childs = []
        for item in self._entries.values():
            if isinstance(item, list):
                childs += item
            elif isinstance(item, dict):
                childs += list(item.values())
            elif item is not None:
                childs.append(item)
        return childs

    def get_pegg(self, _entry=None):
        """
        Returns the top-level Pegg instance.
        """
        if _entry is None: _entry = self
        if _entry._parent is not None:
            _entry = _entry.get_pegg(_entry._parent)
        return _entry

    def get_parent(self):
        """
        Returns the parent EntryType.
        None will be returned if this method is ran from the root (Pegg) instance.
        """
        return self._parent

    def _prettify(self, indentation, compact, _level=0):
        # Lower the _level by one if this is the root of the pegg instance
        _level -= self._parent == None

        kwargs = {
            "indentation":indentation,
            "compact":compact,
            "_level":_level+1}

        content = self.get_content()

        # Set "On one line" to true if compact is set to True and the EntryType contains only one line content.
        on_one_line = compact and (not self.get_childs() and (content is None or "\n" not in content))

        # Start with an empty list
        pretty = []

        # Add the header except if this is the root
        if self._parent is not None:
            pretty.append("{indentation}<{entryType}>{name}{{{separator}".format(
                indentation=indentation*_level,
                entryType=self.__class__.__name__,
                name=" {0} ".format(self._name) if self._name else " ",
                separator=" " if on_one_line else "\n"))

        # Add the content
        if content:
            for line in content.split("\n"):
                pretty.append("{indentation}{line}{separator}".format(
                    indentation="" if on_one_line else indentation*(_level+1),
                    line=line,
                    separator=" " if on_one_line else "\n"))

        # We want the scalers in order which is defined by the _scalers attribute of the class
        if hasattr(self.__class__, "_scalars"):
            for name in [name for name in self.__class__._scalars if name in self._entries["Scalar"]]:
                pretty.append(self._entries["Scalar"][name]._prettify(**kwargs))

        # Here we define the order of how entrytypes are appliad in the egg file.
        for entryname in [
                "Comment", "CoordinateSystem", "Transform", "Matrix3", "Matrix4", "Rotate",
                "MRef", "TRef", "Normal", "Texture", "Material", "VertexPool", "Vertex",
                "VertexRef", "Polygon", "Ref", "Group", "Instance", "UV"]:
            pretty.append(self._get(entryname, **kwargs))

        # Close the EntryType, except if this is the root
        if self._parent is not None:
            pretty.append("{indentation}}}\n".format(indentation="" if on_one_line else indentation*_level))

        # Return the pretty string
        return "".join(pretty)

    def prettify(self, indentation=" "*4, compact=True):
        """
        Returns a string representing the egg format.

        indentation : Default value for indentation is four spaces,
                     other example values are "\t" for one tab indentation or " "*2 for two spaces.
        compact : When set to True EntryType with only one line content and no child entries
                  will be diplayed on the same line.
        """
        return self._prettify(indentation, compact)

    def pprint(self, indentation=" "*4, compact=True, **kwargs):
        print(self._prettify(indentation, compact), **kwargs)

