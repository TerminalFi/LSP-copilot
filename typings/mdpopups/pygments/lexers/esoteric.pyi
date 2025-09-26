from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['BrainfuckLexer', 'BefungeLexer', 'RedcodeLexer']

class BrainfuckLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class BefungeLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class RedcodeLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    opcodes: Incomplete
    modifiers: Incomplete
    tokens: Incomplete
