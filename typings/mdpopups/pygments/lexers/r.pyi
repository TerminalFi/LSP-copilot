from ..lexer import Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['RConsoleLexer', 'SLexer', 'RdLexer']

class RConsoleLexer(Lexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class SLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    builtins_base: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class RdLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
