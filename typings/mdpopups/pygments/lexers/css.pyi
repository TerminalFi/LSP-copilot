from ..lexer import ExtendedRegexLexer, RegexLexer
from _typeshed import Incomplete

__all__ = ['CssLexer', 'SassLexer', 'ScssLexer']

class CssLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class SassLexer(ExtendedRegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class ScssLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
