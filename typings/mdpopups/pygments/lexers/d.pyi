from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['DLexer', 'CrocLexer', 'MiniDLexer']

class DLexer(RegexLexer):
    name: str
    filenames: Incomplete
    aliases: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class CrocLexer(RegexLexer):
    name: str
    filenames: Incomplete
    aliases: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class MiniDLexer(CrocLexer):
    name: str
    filenames: Incomplete
    aliases: Incomplete
    mimetypes: Incomplete
