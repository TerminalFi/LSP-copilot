from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['GAPLexer', 'MathematicaLexer', 'MuPADLexer']

class GAPLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    tokens: Incomplete

class MathematicaLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    operators: Incomplete
    punctuation: Incomplete
    tokens: Incomplete

class MuPADLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    tokens: Incomplete
