from .entrytype import EntryType
from .scalar import MixInScalar
from .tools import fstr, ProtectedDict

class Material(EntryType, MixInScalar):
    _scalars = [
        "diffr", "diffg", "diffb", "diffa", 
        "ambr", "ambg", "ambb", "amba",
        "emitr", "emitg", "emitb", "emita",
        "specr", "specg", "specb", "speca",
        "shininess", "local"] # We don't support local yet, don't understand what the use for local is in this context

    def __init__(self, parent, name):
        super().__init__(parent=parent, name=name)

    def set_diffuse(self, *args, precision=None):
        """
        Accepts diffuse arguments values for: red, green, blue, alpha.
        If less arguments are given, the values are assigned from left to right.
        """
        self.__setrgba(*args, precision=precision, group="diff")

    def set_ambient(self, *args, precision=None):
        """
        Accepts ambient arguments values for: red, green, blue, alpha.
        If less arguments are given, the values are assigned from left to right.
        """
        self.__setrgba(*args, precision=precision, group="amb")

    def set_emission(self, *args, precision=None):
        """
        Accepts emission arguments values for: red, green, blue, alpha.
        If less arguments are given, the values are assigned from left to right.
        """
        self.__setrgba(*args, precision=precision, group="emit")

    def set_specular(self, *args, precision=None):
        """
        Accepts specular arguments values for: red, green, blue, alpha.
        If less arguments are given, the values are assigned from left to right.
        """
        self.__setrgba(*args, precision=precision, group="spec")

    def set_shininess(self, value, precision=None):
        """
        The shininess property controls the size of the specular highlight,
        and the value ranges from 0 to 128.  A larger value creates a
        smaller highlight (creating the appearance of a shinier surface).
        """
        self.add_scaler("shininess", fstr(value, precision))

    def __setrgba(self, *args, precision=None, group=None):
        names = [name for name in self.__class__._scalars if name.startswith(group)]
        for name, value in zip(names, args):
            if value < 0 or value > 1:
                raise ValueError("Invalid value {0} for {1}. Value must between 0.0 and 1.0". format(value, name))
            self.add_scalar(name, fstr(value, precision))

class MixInMaterial:
    def add_material(self, name):
        """
        <Material> name { [scalars] }
    
        This defines a set of material attributes that may later be
        referenced with <MRef> { name }.
    
        The four color groups, diff*, amb*, emit*, and spec* specify the
        diffuse, ambient, emission, and specular components of the lighting
        equation, respectively.  Any of them may be omitted; the omitted
        component(s) take their color from the native color of the
        primitive, otherwise the primitive color is replaced with the
        material color.
        """        
        if name in self._entries["Material"]:
            raise ValueError("Cannot add {0!r}, the material already exists.".format(name))
        material = self._entries["Material"][name] = Material(self, name)
        return material

    @property
    def materials(self):
        return ProtectedDict(self._entries["Material"])