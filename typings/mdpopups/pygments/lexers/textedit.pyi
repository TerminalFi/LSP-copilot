from ..lexer import RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['AwkLexer', 'VimLexer']

class AwkLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class VimLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
    def __init__(self, **options) -> None: ...
    def is_in(self, w, mapping): ...
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
