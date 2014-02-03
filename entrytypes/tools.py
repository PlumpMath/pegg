"""
This is not an EntryType module. Some tools used by EntryTypes are defined here.
"""

def fstr(value, precision):
    """
    Returns typecast to string for the given value if precision is None,
    else a string with float format given the precision.

    examples:
        fstr(3, 3)          --> "3.000"
        fstr(3, None)       --> "3"
        fstr(.123456, None) --> "0.123456"
        fstr(.123456, 4)    --> "0.1235"
        fstr(.999999, 4)    --> "1.0000"
    """
    return str(value) if precision is None else "{0:.{1}f}".format(value, precision)

def strname(name, quote=False):
    """
    Returns a string with a safe name for the egg format.
    - Double quotes are repaced by single quotes.
    - Quotes are added if one of these characters are found: " {}<>",
      or if the quote argument is True
    """
    name = str(name).replace('"', "'")
    if set(" {}<>") & set(name) or quote:
        return '"{0}"'.format(name)
    return name

class ProtectedDict:
    """
    Used to create a protected dictionary from a given dictionary.
    Protected means you can't add, remove or change any values but it's still
    possible to read or iterate the keys and values.
    """
    def __init__(self, dictionary):
        self._dict = dictionary

    def __getitem__(self, key):
        return self._dict[key]

    def __iter__(self):
        for key in self._dict.keys():
            yield key

    def items(self):
        return self._dict.items()

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

if __name__ == "__main__":
    print(fstr(3, 3))
    print(fstr(3, None))
    print(fstr(.123456, None))
    print(fstr(.123456, 4))
    print(fstr(.999999, 4))
    print(strname("{test}"))
    print(strname("Blue 001"))
    print(strname("Blue"))
    print(strname(0))
    d = {"a":3, "b":4}
    pd = ProtectedDict(d)
    print(pd["a"])
    try:
        pd["a"] = 6
    except TypeError:
        print("Good, it's not meant to assign to a protected dict")
    d["a"] = 6
    print(pd["a"])
    for i in pd:
        print(i)



