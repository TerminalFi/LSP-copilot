from ..lexer import Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['PostgresLexer', 'PlPgsqlLexer', 'PostgresConsoleLexer', 'SqlLexer', 'MySqlLexer', 'SqliteConsoleLexer', 'RqlLexer']

class PostgresBase:
    text: Incomplete
    def get_tokens_unprocessed(self, text, *args) -> Generator[Incomplete]: ...

class PostgresLexer(PostgresBase, RegexLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class PlPgsqlLexer(PostgresBase, RegexLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class PsqlRegexLexer(PostgresBase, RegexLexer):
    name: str
    aliases: Incomplete
    flags: Incomplete
    tokens: Incomplete

class lookahead:
    iter: Incomplete
    def __init__(self, x) -> None: ...
    def __iter__(self): ...
    def send(self, i): ...
    def __next__(self): ...
    next = __next__

class PostgresConsoleLexer(Lexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def get_tokens_unprocessed(self, data) -> Generator[Incomplete]: ...

class SqlLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class MySqlLexer(RegexLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class SqliteConsoleLexer(Lexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def get_tokens_unprocessed(self, data) -> Generator[Incomplete]: ...

class RqlLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
