from ..lexer import ExtendedRegexLexer, Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['RubyLexer', 'RubyConsoleLexer', 'FancyLexer']

class RubyLexer(ExtendedRegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    def heredoc_callback(self, match, ctx) -> Generator[Incomplete]: ...
    def gen_rubystrings_rules(): ...
    tokens: Incomplete
    def analyse_text(text): ...

class RubyConsoleLexer(Lexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class FancyLexer(RegexLexer):
    name: str
    filenames: Incomplete
    aliases: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
