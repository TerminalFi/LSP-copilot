from ..lexer import ExtendedRegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['UrbiscriptLexer']

class UrbiscriptLexer(ExtendedRegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    def blob_callback(lexer, match, ctx) -> Generator[Incomplete]: ...
    tokens: Incomplete
