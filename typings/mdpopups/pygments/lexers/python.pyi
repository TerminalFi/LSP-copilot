from ..lexer import Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['PythonLexer', 'PythonConsoleLexer', 'PythonTracebackLexer', 'Python3Lexer', 'Python3TracebackLexer', 'CythonLexer', 'DgLexer', 'NumPyLexer']

class PythonLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class Python3Lexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    uni_name: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class PythonConsoleLexer(Lexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    python3: Incomplete
    def __init__(self, **options) -> None: ...
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class PythonTracebackLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class Python3TracebackLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class CythonLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class DgLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class NumPyLexer(PythonLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    filenames: Incomplete
    EXTRA_KEYWORDS: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
    def analyse_text(text): ...
