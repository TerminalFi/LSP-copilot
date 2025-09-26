from ..lexer import RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['ZephirLexer', 'PhpLexer']

class ZephirLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    zephir_keywords: Incomplete
    zephir_type: Incomplete
    flags: Incomplete
    tokens: Incomplete

class PhpLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
    funcnamehighlighting: Incomplete
    disabledmodules: Incomplete
    startinline: Incomplete
    def __init__(self, **options) -> None: ...
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
    def analyse_text(text): ...
