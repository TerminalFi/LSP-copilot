from ..lexer import DelegatingLexer, RegexLexer
from _typeshed import Incomplete

__all__ = ['CSharpLexer', 'NemerleLexer', 'BooLexer', 'VbNetLexer', 'CSharpAspxLexer', 'VbNetAspxLexer', 'FSharpLexer']

class CSharpLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    levels: Incomplete
    tokens: Incomplete
    token_variants: bool
    def __init__(self, **options) -> None: ...

class NemerleLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    levels: Incomplete
    tokens: Incomplete
    token_variants: bool
    def __init__(self, **options) -> None: ...

class BooLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class VbNetLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    uni_name: Incomplete
    flags: Incomplete
    tokens: Incomplete
    def analyse_text(text): ...

class GenericAspxLexer(RegexLexer):
    name: str
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class CSharpAspxLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class VbNetAspxLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...
    def analyse_text(text): ...

class FSharpLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    keywords: Incomplete
    keyopts: Incomplete
    operators: str
    word_operators: Incomplete
    prefix_syms: str
    infix_syms: str
    primitives: Incomplete
    tokens: Incomplete
