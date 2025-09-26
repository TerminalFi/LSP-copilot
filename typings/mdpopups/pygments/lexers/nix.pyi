from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['NixLexer']

class NixLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    keywords: Incomplete
    builtins: Incomplete
    operators: Incomplete
    punctuations: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...
