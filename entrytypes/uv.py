from .entrytype import EntryType
from .tools import fstr, ProtectedDict

class UV(EntryType):
    def __init__(self, parent, u, v, w=None, name=None, precision=None): # Name can be None for an UV EntryType
        super().__init__(parent=parent, name=name)
        self._precision = precision
        self._co = [value for value in [u, v, w] if value is not None]

    def get_content(self):
        return " ".join(map(lambda value: fstr(value, self._precision), self._co))

    @property
    def co(self):
        return self._co

class MixInUV:
    def add_uv(self, u, v, w=None, name=None, precision=None):
        """
        <UV> [name] { u v [w] [tangent] [binormal] [morph-list] }

        This gives the texture coordinates of the vertex.  This must be
        specified if a texture is to be mapped onto this geometry.

        The texture coordinates are usually two-dimensional, with two
        component values (u v), but they may also be three-dimensional,
        with three component values (u v w).  (Arguably, it should be
        called <UVW> instead of <UV> in the three-dimensional case, but
        it's not.)

        As before, morph-list is an optional list of <DUV> entries.

        Unlike the other kinds of attributes, there may be multiple sets
        of UV's on each vertex, each with a unique name; This name is a reference
        to a texture. Be sure a texture with a scalar for uv-name exists.
        The name may be omitted to specify the default UV's.

        The UV's also support an optional tangent and binormal.  These
        values are based on the vertex normal and the UV coordinates of
        connected vertices, and are used to render normal maps and similar
        lighting effects.  They are defined within the <UV> entry because
        there may be a different set of tangents and binormals for each
        different UV coordinate set.  If present, they have the expected
        syntax: <UV> [name] { u v [w] <Tangent> { x y z } <Binormal> { x y z } }
        """
        name = None if name in ["", None] else str(name) # Replace "" with None and make sure 0 translates to string "0".
        if name in self._entries["UV"]:
            raise ValueError("Cannot add {0!r}, the UV already exists.".format("default" if name is None else name))
        if name is not None and name not in [texentry.get_scalar("uv-name") for texentry in self.get_pegg().textures.values()]:
            raise ValueError("Cannot add {0!r}, there is not texture with a reference to this uv-name.".format(name))
        uv = self._entries["UV"][name] = UV(self, u, v, w, name, precision=precision)
        return uv

    @property
    def uvs(self):
        """
        Returns a dict of all UV's. UVs[None] will return the Default UV if set.
        """
        return ProtectedDict(self._entries["UV"])

    @property
    def uv(self):
        """
        Returns the default UV (UVs[None]) if set, else return None
        """
        return self._entries["UV"].get(None, None)

