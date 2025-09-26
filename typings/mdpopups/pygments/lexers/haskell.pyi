from ..lexer import Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['HaskellLexer', 'IdrisLexer', 'AgdaLexer', 'CryptolLexer', 'LiterateHaskellLexer', 'LiterateIdrisLexer', 'LiterateAgdaLexer', 'LiterateCryptolLexer', 'KokaLexer']

class HaskellLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    reserved: Incomplete
    ascii: Incomplete
    tokens: Incomplete

class IdrisLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    reserved: Incomplete
    ascii: Incomplete
    directives: Incomplete
    tokens: Incomplete

class AgdaLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    reserved: Incomplete
    tokens: Incomplete

class CryptolLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    reserved: Incomplete
    ascii: Incomplete
    tokens: Incomplete
    EXTRA_KEYWORDS: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class LiterateLexer(Lexer):
    bird_re: Incomplete
    baselexer: Incomplete
    def __init__(self, baselexer, **options) -> None: ...
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class LiterateHaskellLexer(LiterateLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class LiterateIdrisLexer(LiterateLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class LiterateAgdaLexer(LiterateLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class LiterateCryptolLexer(LiterateLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class KokaLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    keywords: Incomplete
    typeStartKeywords: Incomplete
    typekeywords: Incomplete
    builtin: Incomplete
    symbols: str
    sboundary: Incomplete
    boundary: str
    tokenType: Incomplete
    tokenTypeDef: Incomplete
    tokenConstructor: Incomplete
    tokens: Incomplete
