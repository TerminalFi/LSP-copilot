from ..lexer import ExtendedRegexLexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['PerlLexer', 'Perl6Lexer']

class PerlLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class Perl6Lexer(ExtendedRegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    PERL6_IDENTIFIER_RANGE: str
    PERL6_KEYWORDS: Incomplete
    PERL6_BUILTINS: Incomplete
    PERL6_BUILTIN_CLASSES: Incomplete
    PERL6_OPERATORS: Incomplete
    PERL6_BRACKETS: Incomplete
    def brackets_callback(token_class): ...
    def opening_brace_callback(lexer, match, context) -> Generator[Incomplete]: ...
    def closing_brace_callback(lexer, match, context) -> Generator[Incomplete]: ...
    def embedded_perl6_callback(lexer, match, context) -> Generator[Incomplete]: ...
    tokens: Incomplete
    def analyse_text(text): ...
    encoding: Incomplete
    def __init__(self, **options) -> None: ...
