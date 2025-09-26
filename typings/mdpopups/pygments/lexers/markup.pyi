from ..lexer import DelegatingLexer, RegexLexer
from _typeshed import Incomplete

__all__ = ['BBCodeLexer', 'MoinWikiLexer', 'RstLexer', 'TexLexer', 'GroffLexer', 'MozPreprocHashLexer', 'MozPreprocPercentLexer', 'MozPreprocXulLexer', 'MozPreprocJavascriptLexer', 'MozPreprocCssLexer']

class BBCodeLexer(RegexLexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class MoinWikiLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class RstLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    closers: str
    unicode_delimiters: str
    end_string_suffix: Incomplete
    tokens: Incomplete
    handlecodeblocks: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class TexLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class GroffLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class MozPreprocHashLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class MozPreprocPercentLexer(MozPreprocHashLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class MozPreprocXulLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class MozPreprocJavascriptLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class MozPreprocCssLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
