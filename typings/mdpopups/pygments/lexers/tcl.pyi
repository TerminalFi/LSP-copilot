from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['TclLexer']

class TclLexer(RegexLexer):
    keyword_cmds_re: Incomplete
    builtin_cmds_re: Incomplete
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...
