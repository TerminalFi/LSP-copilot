from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['ResourceLexer']

class ResourceLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    flags: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...
