from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['ModelicaLexer', 'BugsLexer', 'JagsLexer', 'StanLexer']

class ModelicaLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class BugsLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class JagsLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class StanLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...
