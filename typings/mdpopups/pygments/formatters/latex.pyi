from ..formatter import Formatter
from ..lexer import Lexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['LatexFormatter']

class LatexFormatter(Formatter):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    docclass: Incomplete
    preamble: Incomplete
    linenos: Incomplete
    linenostart: Incomplete
    linenostep: Incomplete
    verboptions: Incomplete
    nobackground: Incomplete
    commandprefix: Incomplete
    texcomments: Incomplete
    mathescape: Incomplete
    escapeinside: Incomplete
    left: Incomplete
    right: Incomplete
    envname: Incomplete
    def __init__(self, **options) -> None: ...
    def get_style_defs(self, arg: str = ''): ...
    def format_unencoded(self, tokensource, outfile) -> None: ...

class LatexEmbeddedLexer(Lexer):
    left: Incomplete
    right: Incomplete
    lang: Incomplete
    def __init__(self, left, right, lang, **options) -> None: ...
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
    def get_tokens_aux(self, index, text) -> Generator[Incomplete]: ...
