from ..lexer import RegexLexer
from ..token import Operator, String, Text
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['IrcLogsLexer', 'TodotxtLexer', 'HttpLexer', 'GettextLexer']

class IrcLogsLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    timestamp: str
    tokens: Incomplete

class GettextLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class HttpLexer(RegexLexer):
    name: str
    aliases: Incomplete
    flags: Incomplete
    content_type: Incomplete
    def header_callback(self, match) -> Generator[Incomplete]: ...
    def continuous_header_callback(self, match) -> Generator[Incomplete]: ...
    def content_callback(self, match) -> Generator[Incomplete]: ...
    tokens: Incomplete
    def analyse_text(text): ...

class TodotxtLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    CompleteTaskText = Operator
    IncompleteTaskText = Text
    Priority: Incomplete
    Date: Incomplete
    Project: Incomplete
    Context = String
    date_regex: str
    priority_regex: str
    project_regex: str
    context_regex: str
    complete_one_date_regex: Incomplete
    complete_two_date_regex: Incomplete
    priority_date_regex: Incomplete
    tokens: Incomplete
