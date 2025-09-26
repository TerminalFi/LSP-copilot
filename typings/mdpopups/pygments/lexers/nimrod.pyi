from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['NimrodLexer']

class NimrodLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    def underscorize(words): ...
    keywords: Incomplete
    keywordsPseudo: Incomplete
    opWords: Incomplete
    types: Incomplete
    tokens: Incomplete
