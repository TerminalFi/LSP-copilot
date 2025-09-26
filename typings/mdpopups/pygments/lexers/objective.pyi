from ..lexer import RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['ObjectiveCLexer', 'ObjectiveCppLexer', 'LogosLexer', 'SwiftLexer']

class ObjectiveCLexer(Incomplete):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    priority: float

class ObjectiveCppLexer(Incomplete):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    priority: float

class LogosLexer(ObjectiveCppLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    priority: float
    tokens: Incomplete
    def analyse_text(text): ...

class SwiftLexer(RegexLexer):
    name: str
    filenames: Incomplete
    aliases: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
