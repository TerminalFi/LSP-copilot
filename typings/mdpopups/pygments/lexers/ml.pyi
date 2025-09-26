from ..lexer import RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['SMLLexer', 'OcamlLexer', 'OpaLexer']

class SMLLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    alphanumid_reserved: Incomplete
    symbolicid_reserved: Incomplete
    nonid_reserved: Incomplete
    alphanumid_re: str
    symbolicid_re: str
    def stringy(whatkind): ...
    def long_id_callback(self, match) -> Generator[Incomplete]: ...
    def end_id_callback(self, match) -> Generator[Incomplete]: ...
    def id_callback(self, match) -> Generator[Incomplete]: ...
    tokens: Incomplete

class OcamlLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    keywords: Incomplete
    keyopts: Incomplete
    operators: str
    word_operators: Incomplete
    prefix_syms: str
    infix_syms: str
    primitives: Incomplete
    tokens: Incomplete

class OpaLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    keywords: Incomplete
    ident_re: str
    op_re: str
    punc_re: str
    tokens: Incomplete
