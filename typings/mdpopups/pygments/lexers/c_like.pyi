from ..lexer import RegexLexer
from .c_cpp import CLexer, CppLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['PikeLexer', 'NesCLexer', 'ClayLexer', 'ECLexer', 'ValaLexer', 'CudaLexer', 'SwigLexer', 'MqlLexer', 'ArduinoLexer']

class PikeLexer(CppLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class NesCLexer(CLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class ClayLexer(RegexLexer):
    name: str
    filenames: Incomplete
    aliases: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class ECLexer(CLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class ValaLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class CudaLexer(CLexer):
    name: str
    filenames: Incomplete
    aliases: Incomplete
    mimetypes: Incomplete
    function_qualifiers: Incomplete
    variable_qualifiers: Incomplete
    vector_types: Incomplete
    variables: Incomplete
    functions: Incomplete
    execution_confs: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class SwigLexer(CppLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    priority: float
    tokens: Incomplete
    swig_directives: Incomplete
    def analyse_text(text): ...

class MqlLexer(CppLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class ArduinoLexer(CppLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    constants: Incomplete
    structure: Incomplete
    storage: Incomplete
    functions: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
