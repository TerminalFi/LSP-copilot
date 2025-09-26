from ..lexer import Lexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['TextLexer', 'RawTokenLexer']

class TextLexer(Lexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class RawTokenLexer(Lexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    compress: Incomplete
    def __init__(self, **options) -> None: ...
    def get_tokens(self, text) -> Generator[Incomplete]: ...
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
