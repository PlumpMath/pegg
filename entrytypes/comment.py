from .entrytype import EntryType
from .tools import strname

class Comment(EntryType):
    def __init__(self, parent, comment):
        super().__init__(parent=parent)
        self._comment = strname(comment, quote=True)

    def get_content(self):
        return self._comment

class MixInComment:
    def append_comment(self, comment):
        """
        <Comment> { text }

        <Comment> entries are slightly different, in that tools which read and
        write egg files will preserve the text within <Comment> entries, but
        they may not preserve comments delimited by // or /* */.  Special
        characters and keywords within a <Comment> entry should be quoted;
        it's safest to quote the entire comment.
        """
        self._entries["Comment"].append(Comment(self, comment))
