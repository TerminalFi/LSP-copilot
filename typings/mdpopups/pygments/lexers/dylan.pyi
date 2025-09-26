from ..lexer import Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['DylanLexer', 'DylanConsoleLexer', 'DylanLidLexer']

class DylanLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    builtins: Incomplete
    keywords: Incomplete
    operators: Incomplete
    functions: Incomplete
    valid_name: str
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
    tokens: Incomplete

class DylanLidLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class DylanConsoleLexer(Lexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
