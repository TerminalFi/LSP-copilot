from ..lexer import Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['MatlabLexer', 'MatlabSessionLexer', 'OctaveLexer', 'ScilabLexer']

class MatlabLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    elfun: Incomplete
    specfun: Incomplete
    elmat: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class MatlabSessionLexer(Lexer):
    name: str
    aliases: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class OctaveLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    builtin_kw: Incomplete
    command_kw: Incomplete
    function_kw: Incomplete
    loadable_kw: Incomplete
    mapping_kw: Incomplete
    builtin_consts: Incomplete
    tokens: Incomplete

class ScilabLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
