from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['DiffLexer', 'DarcsPatchLexer']

class DiffLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class DarcsPatchLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    DPATCH_KEYWORDS: Incomplete
    tokens: Incomplete
