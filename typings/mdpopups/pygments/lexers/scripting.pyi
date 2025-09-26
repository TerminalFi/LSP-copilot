from ..lexer import RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['LuaLexer', 'MoonScriptLexer', 'ChaiscriptLexer', 'LSLLexer', 'AppleScriptLexer', 'RexxLexer', 'MOOCodeLexer', 'HybrisLexer']

class LuaLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    func_name_highlighting: Incomplete
    disabled_modules: Incomplete
    def __init__(self, **options) -> None: ...
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class MoonScriptLexer(LuaLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class ChaiscriptLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete

class LSLLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    lsl_keywords: str
    lsl_types: str
    lsl_states: str
    lsl_events: str
    lsl_functions_builtin: str
    lsl_constants_float: str
    lsl_constants_integer: str
    lsl_constants_integer_boolean: str
    lsl_constants_rotation: str
    lsl_constants_string: str
    lsl_constants_vector: str
    lsl_invalid_broken: str
    lsl_invalid_deprecated: str
    lsl_invalid_illegal: str
    lsl_invalid_unimplemented: str
    lsl_reserved_godmode: str
    lsl_reserved_log: str
    lsl_operators: str
    tokens: Incomplete

class AppleScriptLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    flags: Incomplete
    Identifiers: str
    Literals: Incomplete
    Classes: Incomplete
    BuiltIn: Incomplete
    HandlerParams: Incomplete
    Commands: Incomplete
    References: Incomplete
    Operators: Incomplete
    Control: Incomplete
    Declarations: Incomplete
    Reserved: Incomplete
    StudioClasses: Incomplete
    StudioEvents: Incomplete
    StudioCommands: Incomplete
    StudioProperties: Incomplete
    tokens: Incomplete

class RexxLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
    PATTERNS_AND_WEIGHTS: Incomplete
    def analyse_text(text): ...

class MOOCodeLexer(RegexLexer):
    name: str
    filenames: Incomplete
    aliases: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete

class HybrisLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    tokens: Incomplete
