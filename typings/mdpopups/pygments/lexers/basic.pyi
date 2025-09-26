from ..lexer import RegexLexer
from _typeshed import Incomplete

__all__ = ['BlitzBasicLexer', 'BlitzMaxLexer', 'MonkeyLexer', 'CbmBasicV2Lexer', 'QBasicLexer']

class BlitzMaxLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    bmax_vopwords: str
    bmax_sktypes: str
    bmax_lktypes: str
    bmax_name: str
    bmax_var: Incomplete
    bmax_func: Incomplete
    flags: Incomplete
    tokens: Incomplete

class BlitzBasicLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    bb_sktypes: str
    bb_name: str
    bb_var: Incomplete
    flags: Incomplete
    tokens: Incomplete

class MonkeyLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    name_variable: str
    name_function: str
    name_constant: str
    name_class: str
    name_module: str
    keyword_type: str
    keyword_type_special: str
    flags: Incomplete
    tokens: Incomplete

class CbmBasicV2Lexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    flags: Incomplete
    tokens: Incomplete
    def analyse_text(self, text): ...

class QBasicLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    declarations: Incomplete
    functions: Incomplete
    metacommands: Incomplete
    operators: Incomplete
    statements: Incomplete
    keywords: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...
