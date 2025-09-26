from ..lexer import Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['MakefileLexer', 'BaseMakefileLexer', 'CMakeLexer']

class MakefileLexer(Lexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    r_special: Incomplete
    r_comment: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
    def analyse_text(text): ...

class BaseMakefileLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class CMakeLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...
