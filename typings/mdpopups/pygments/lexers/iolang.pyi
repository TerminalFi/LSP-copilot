from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['IoLexer']

class IoLexer(RegexLexer):
    name: str
    filenames: Incomplete
    aliases: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
