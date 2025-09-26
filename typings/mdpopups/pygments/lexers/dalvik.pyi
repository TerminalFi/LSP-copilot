from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['SmaliLexer']

class SmaliLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...
