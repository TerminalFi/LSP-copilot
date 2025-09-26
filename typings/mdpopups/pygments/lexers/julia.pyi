from ..lexer import Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['JuliaLexer', 'JuliaConsoleLexer']

class JuliaLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    builtins: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class JuliaConsoleLexer(Lexer):
    name: str
    aliases: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
