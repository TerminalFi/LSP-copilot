from ..lexer import RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['CLexer', 'CppLexer']

class CFamilyLexer(RegexLexer):
    tokens: Incomplete
    stdlib_types: Incomplete
    c99_types: Incomplete
    stdlibhighlighting: Incomplete
    c99highlighting: Incomplete
    def __init__(self, **options) -> None: ...
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class CLexer(CFamilyLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    priority: float
    def analyse_text(text): ...

class CppLexer(CFamilyLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    priority: float
    tokens: Incomplete
    def analyse_text(text): ...
