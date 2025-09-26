from ..lexer import RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['RebolLexer', 'RedLexer']

class RebolLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    escape_re: str
    def word_callback(lexer, match) -> Generator[Incomplete]: ...
    tokens: Incomplete
    def analyse_text(text): ...

class RedLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    escape_re: str
    def word_callback(lexer, match) -> Generator[Incomplete]: ...
    tokens: Incomplete
