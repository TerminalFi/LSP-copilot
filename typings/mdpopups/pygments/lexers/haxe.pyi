from ..lexer import ExtendedRegexLexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['HaxeLexer', 'HxmlLexer']

class HaxeLexer(ExtendedRegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    keyword: str
    typeid: str
    ident: Incomplete
    binop: str
    ident_no_keyword: Incomplete
    flags: Incomplete
    preproc_stack: Incomplete
    def preproc_callback(self, match, ctx) -> Generator[Incomplete]: ...
    tokens: Incomplete
    def analyse_text(text): ...

class HxmlLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    tokens: Incomplete
