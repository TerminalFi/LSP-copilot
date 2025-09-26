from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['NSISLexer', 'RPMSpecLexer', 'SourcesListLexer', 'DebianControlLexer']

class NSISLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class RPMSpecLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class SourcesListLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetype: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class DebianControlLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    tokens: Incomplete
