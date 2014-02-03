from .entrytype import EntryType
from .scalar import MixInScalar
from .transform import MixInTransform
from .tools import fstr, strname, ProtectedDict

class Texture(EntryType, MixInScalar, MixInTransform):
    _scalars = [
        "alpha-file", "alpha-file-channel", "format", "compression",
        "wrap", "wrapu", "wrapv", "wrapw", "borderr", "borderg", "borderb", "bordera",
        "type", "multiview", "num-views", "envtype", "uv-name"] # We don't support wrapw yet, Panda3D is currently not supporting this scalar

    def __init__(self, parent, name, filename):
        super().__init__(parent=parent, name=name)
        self._filename = str(filename)

    def get_content(self):
        return '"' + self._filename + '"'

    def __set_wrap(self, name, repeat_definition):
        self.__set_uppercase_value(name, repeat_definition, (
            "CLAMP", "REPEAT", "MIRROR", "MIRROR_ONCE", "BORDER_COLOR"))

    def __setrgba(self, *args, precision=None, group=None):
        names = [name for name in self.__class__._scalars if name.startswith(group)]
        for name, value in zip(names, args):
            if not 0 <= value <= 1:
                raise ValueError("Invalid value {0} for {1}. Value must between 0.0 and 1.0". format(value, name))
            self.add_scalar(name, fstr(value, precision))

    def __set_uppercase_value(self, name, value, valid):
        value = value.upper()
        if not value in valid:
            raise ValueError("Invalid value for {0!r}: {1}. Valid values are {2}".format(name, value, ", ".join(valid)))
        self.add_scalar(name, value)

    def set_alpha_file(self, filename):
        """
        <Scalar> alpha-file { alpha-filename }

        If this scalar is present, the texture file's alpha channel is
        read in from the named image file (which should contain a
        grayscale image), and the two images are combined into a single
        two- or four-channel image internally.  This is useful for loading
        alpha channels along with image file formats like JPEG that don't
        traditionally support alpha channels.
        """
        self.add_scalar("alpha-file", filename)

    def set_alpha_file_channel(self, channel=0):
        """
        <Scalar> alpha-file-channel { channel }

        This defines the channel that should be extracted from the file
        named by alpha-file to determine the alpha channel for the
        resulting channel.  The default is 0, which means the grayscale
        combination of r, g, b.  Otherwise, this should be the 1-based
        channel number, for instance 1, 2, or 3 for r, g, or b,
        respectively, or 4 for the alpha channel of a four-component
        image.
        """
        if not channel in range(5):
            raise ValueError("Invalid channel '{0}'. Valid channels are {1}".format(channel, ", ".join(map(str, range(5)))))
        self.add_scalar("alpha-file-channel", channel)

    def set_format(self, format):
        """
        <Scalar> format { format-definition }

        This defines the load format of the image file.  The
        format-definition is one of:
          RGBA, RGBM, RGBA12, RGBA8, RGBA4,
          RGB, RGB12, RGB8, RGB5, RGB332,
          LUMINANCE_ALPHA,
          RED, GREEN, BLUE, ALPHA, LUMINANCE

        The formats whose names end in digits specifically request a
        particular texel width.  RGB12 and RGBA12 specify 48-bit texels
        with or without alpha; RGB8 and RGBA8 specify 32-bit texels, and
        RGB5 and RGBA4 specify 16-bit texels.  RGB332 specifies 8-bit
        texels.

        The remaining formats are generic and specify only the semantic
        meaning of the channels.  The size of the texels is determined by
        the width of the components in the image file.  RGBA is the most
        general; RGB is the same, but without any alpha channel.  RGBM is
        like RGBA, except that it requests only one bit of alpha, if the
        graphics card can provide that, to leave more room for the RGB
        components, which is especially important for older 16-bit
        graphics cards (the "M" stands for "mask", as in a cutout).

        The number of components of the image file should match the format
        specified; if it does not, the egg loader will attempt to provide
        the closest match that does.
        """
        self.__set_uppercase_value("format", format, (
            "RGBA", "RGBM", "RGBA12", "RGBA8", "RGBA4",
            "RGB", "RGB12", "RGB8", "RGB5", "RGB332", "LUMINANCE_ALPHA",
            "RED", "GREEN", "BLUE", "ALPHA", "LUMINANCE"))

    def set_compression(self, compression="DEFAULT"):
        """
        <Scalar> compression { compression-mode }

        Defines an explicit control over the real-time compression mode applied to the texture.
        The various options are: DEFAULT OFF ON FXT1 DXT1 DXT2 DXT3 DXT4 DXT5

        This controls the compression of the texture when it is loaded
        into graphics memory, and has nothing to do with on-disk
        compression such as JPEG.  If this option is omitted or "DEFAULT",
        then the texture compression is controlled by the
        compressed-textures config variable.  If it is "OFF", texture
        compression is explicitly off for this texture regardless of the
        setting of the config variable; if it is "ON", texture compression
        is explicitly on, and a default compression algorithm supported by
        the driver is selected.  If any of the other options, it names the
        specific compression algorithm to be used.
        """
        self.__set_uppercase_value("compression", compression, (
            "DEFAULT", "OFF", "ON", "FXT1", "DXT1", "DXT2", "DXT3", "DXT4", "DXT5"))

    def set_wrap(self, repeat_definition):
        """
        <Scalar> wrap { repeat-definition }

        This defines the behavior of the texture image outside of the
        normal (u,v) range 0.0 - 1.0.  It is "REPEAT" to repeat the
        texture to infinity, "CLAMP" not to.  The wrapping behavior may be
        specified independently for each axis via "wrapu" and "wrapv", or
        it may be specified for both simultaneously via "wrap".

        There are other legal values in addtional to REPEAT and CLAMP.
        The full list is: CLAMP REPEAT MIRROR MIRROR_ONCE BORDER_COLOR
        """
        self.__set_wrap("wrap", repeat_definition)

    def set_wrapu(self, repeat_definition):
        """
        <Scalar> wrapu { repeat-definition }

        See 'set_wrap()' for a full explanation of this method.
        """
        self.__set_wrap("wrapu", repeat_definition)

    def set_wrapv(self, repeat_definition):
        """
        <Scalar> wrapv { repeat-definition }

        See 'set_wrap()' for a full explanation of this method.
        """
        self.__set_wrap("wrapv", repeat_definition)

    def set_border_color(self, *args, precision=None):
        """
        <Scalar> borderr, <Scalar> borderg <Scalar> borderb, <Scalar> bordera { color }

        Accepts border color arguments values for:  red, green, blue, alpha.
        If less arguments are given, the values are assigned from left to right.

        The border color is particularly important when one of the wrap modes,
        is BORDER_COLOR. (see 'set_wrap()' method for more info)
        """
        self.__setrgba(*args, precision=precision, group="border")

    def set_type(self, texture_type="2D"):
        """
        <Scalar> type { texture-type }

        This may be one of the following attributes: 1D 2D 3D CUBE_MAP

        The default is "2D", which specifies a normal, 2-d texture.  If
        any of the other types is specified instead, a texture image of
        the corresponding type is loaded.

        If 3D or CUBE_MAP is specified, then a series of texture images
        must be loaded to make up the complete texture; in this case, the
        texture filename is expected to include a sequence of one or more
        hash mark ("#") characters, which will be filled in with the
        sequence number.  The first image in the sequence must be numbered
        0, and there must be no gaps in the sequence.  In this case, a
        separate alpha-file designation is ignored; the alpha channel, if
        present, must be included in the same image with the color
        channel(s).
        """
        self.__set_uppercase_value("type", texture_type, ("1D", "2D", "3D", "CUBE_MAP"))

    def set_multiview(self, flag, precision=None):
        """
        <Scalar> multiview { flag }

        If this flag is nonzero, the texture is loaded as a multiview
        texture.  In this case, the filename must contain a hash mark
        ("#") as in the 3D or CUBE_MAP case, above, and the different
        images are loaded into the different views of the multiview
        textures.  If the texture is already a cube map texture, the
        same hash sequence is used for both purposes: the first six images
        define the first view, the next six images define the second view,
        and so on.  If the texture is a 3-D texture, you must also specify
        num-views, below, to tell the loader how many images are loaded
        for views, and how many are loaded for levels.

        A multiview texture is most often used to load stereo textures,
        where a different image is presented to each eye viewing the
        texture, but other uses are possible, such as for texture
        animation.
        """
        if not 0 <= flag <= 1:
            raise ValueError("Invalid flag {0} for multiview. Value must between 0.0 and 1.0". format(flag))
        self.add_scalar("multiview", fstr(flag, precision))

    def set_num_views(self, count):
        """
        <Scalar> num-views { count }

        This is used only when loading a 3-D multiview texture.  It
        specifies how many different views the texture holds; the z height
        of the texture is then implicitly determined as (number of images)
        """
        if not isinstance(count, int):
            raise TypeError("count must be of type 'int', not {0}".format(type(count)))
        if count < 1:
            raise ValueError("Invalid count value: {0}, value must be at least one or higher".format(count))
        self.__add_scalar("num-views", count)

    def set_envtype(self, envtype="MODULATE"):
        """
        <Scalar> envtype { environment-type }

        This specifies the type of texture environment to create; i.e. it
        controls the way in which textures apply to models.
        Environment-type may be one of:

          MODULATE
          DECAL
          BLEND
          REPLACE
          ADD
          BLEND_COLOR_SCALE
          MODULATE_GLOW
          MODULATE_GLOSS
         *NORMAL
         *NORMAL_HEIGHT
         *GLOW
         *GLOSS
         *HEIGHT
         *SELECTOR

        The default environment type is MODULATE, which means the texture
        color is multiplied with the base polygon (or vertex) color.  This
        is the most common texture environment by far.  Other environment
        types are more esoteric and are especially useful in the presence
        of multitexture.  In particular, the types prefixed by an asterisk
        (*) require enabling Panda's automatic ShaderGenerator.
        """
        self.__set_uppercase_value("envtype", envtype, (
            "MODULATE", "DECAL", "BLEND", "REPLACE", "ADD", "BLEND_COLOR_SCALE", "MODULATE_GLOW", "MODULATE_GLOSS"))

    def set_uv_name(self, uv_name):
        """
        <Scalar> uv-name { name }

        Specifies the name of the texture coordinates that are to be
        associated with this texture.  If this is omitted, the default
        texture coordinates are used.
        """
        self.add_scalar("uv-name", strname(uv_name))


class MixInTexture:
    def add_texture(self, name, filename):
        """
        <Texture> name { filename [scalars] }

        This describes a texture file that can be referenced later with
        <TRef> { name }.  It is not necessary to make a <Texture> entry for
        each texture to be used; a texture may also be referenced directly
        by the geometry via an abbreviated inline <Texture> entry, but a
        separate <Texture> entry is the only way to specify anything other
        than the default texture attributes.

        If the filename is a relative path, the current egg file's directory
        is searched first, and then the texture-path and model-path are
        searched.
        """
        if name in self._entries["Texture"]:
            raise TextureExistError("Cannot add {0!r}, the texture already exists.".format(name))
        texture = self._entries["Texture"][name] = Texture(self, name, filename)
        return texture

    @property
    def textures(self):
        return ProtectedDict(self._entries["Texture"])
