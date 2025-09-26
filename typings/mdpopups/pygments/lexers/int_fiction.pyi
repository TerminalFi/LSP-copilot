from ..lexer import RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['Inform6Lexer', 'Inform6TemplateLexer', 'Inform7Lexer', 'Tads3Lexer']

class Inform6Lexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    flags: Incomplete
    tokens: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class Inform7Lexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    flags: Incomplete
    tokens: Incomplete
    token_variants: Incomplete
    def __init__(self, **options) -> None: ...

class Inform6TemplateLexer(Inform7Lexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def get_tokens_unprocessed(self, text, stack=('+i6t-root',)): ...

class Tads3Lexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    flags: Incomplete
    tokens: Incomplete
    def get_tokens_unprocessed(self, text, **kwargs) -> Generator[Incomplete]: ...
