from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['ActionScriptLexer', 'ActionScript3Lexer', 'MxmlLexer']

class ActionScriptLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class ActionScript3Lexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    identifier: str
    typeidentifier: Incomplete
    flags: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class MxmlLexer(RegexLexer):
    flags: Incomplete
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetimes: Incomplete
    tokens: Incomplete
