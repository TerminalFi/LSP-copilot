from ..lexer import RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['SchemeLexer', 'CommonLispLexer', 'HyLexer', 'RacketLexer', 'NewLispLexer', 'EmacsLispLexer']

class SchemeLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    keywords: Incomplete
    builtins: Incomplete
    valid_name: str
    tokens: Incomplete

class CommonLispLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    nonmacro: str
    constituent: Incomplete
    terminated: str
    symbol: Incomplete
    builtin_function: Incomplete
    special_forms: Incomplete
    macros: Incomplete
    lambda_list_keywords: Incomplete
    declarations: Incomplete
    builtin_types: Incomplete
    builtin_classes: Incomplete
    def __init__(self, **options) -> None: ...
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
    tokens: Incomplete

class HyLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    special_forms: Incomplete
    declarations: Incomplete
    hy_builtins: Incomplete
    hy_core: Incomplete
    builtins: Incomplete
    valid_name: str
    tokens: Incomplete
    def analyse_text(text): ...

class RacketLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class NewLispLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    builtins: Incomplete
    valid_name: str
    tokens: Incomplete

class EmacsLispLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    nonmacro: str
    constituent: Incomplete
    terminated: str
    symbol: Incomplete
    macros: Incomplete
    special_forms: Incomplete
    builtin_function: Incomplete
    builtin_function_highlighted: Incomplete
    lambda_list_keywords: Incomplete
    error_keywords: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
    tokens: Incomplete
