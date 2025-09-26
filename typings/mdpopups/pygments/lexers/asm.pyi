from ..lexer import DelegatingLexer, RegexLexer
from _typeshed import Incomplete

__all__ = ['GasLexer', 'ObjdumpLexer', 'DObjdumpLexer', 'CppObjdumpLexer', 'CObjdumpLexer', 'LlvmLexer', 'NasmLexer', 'NasmObjdumpLexer', 'Ca65Lexer']

class GasLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    string: str
    char: str
    identifier: Incomplete
    number: str
    tokens: Incomplete
    def analyse_text(text): ...

class ObjdumpLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class DObjdumpLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class CppObjdumpLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class CObjdumpLexer(DelegatingLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def __init__(self, **options) -> None: ...

class LlvmLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    string: str
    identifier: Incomplete
    tokens: Incomplete

class NasmLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    identifier: str
    hexn: str
    octn: str
    binn: str
    decn: str
    floatn: Incomplete
    string: Incomplete
    declkw: str
    register: str
    wordop: str
    type: str
    directives: str
    flags: Incomplete
    tokens: Incomplete

class NasmObjdumpLexer(ObjdumpLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class Ca65Lexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    flags: Incomplete
    tokens: Incomplete
    def analyse_text(self, text): ...
