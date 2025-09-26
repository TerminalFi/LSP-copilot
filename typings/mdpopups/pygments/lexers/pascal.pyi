from ..lexer import Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['DelphiLexer', 'AdaLexer']

class DelphiLexer(Lexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    TURBO_PASCAL_KEYWORDS: Incomplete
    DELPHI_KEYWORDS: Incomplete
    FREE_PASCAL_KEYWORDS: Incomplete
    BLOCK_KEYWORDS: Incomplete
    FUNCTION_MODIFIERS: Incomplete
    DIRECTIVES: Incomplete
    BUILTIN_TYPES: Incomplete
    BUILTIN_UNITS: Incomplete
    ASM_REGISTERS: Incomplete
    ASM_INSTRUCTIONS: Incomplete
    keywords: Incomplete
    builtins: Incomplete
    def __init__(self, **options) -> None: ...
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class AdaLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
