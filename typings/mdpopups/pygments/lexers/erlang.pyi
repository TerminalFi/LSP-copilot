from ..lexer import Lexer, RegexLexer
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['ErlangLexer', 'ErlangShellLexer', 'ElixirConsoleLexer', 'ElixirLexer']

class ErlangLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    keywords: Incomplete
    builtins: Incomplete
    operators: str
    word_operators: Incomplete
    atom_re: str
    variable_re: str
    escape_re: str
    macro_re: Incomplete
    base_re: str
    tokens: Incomplete

class ErlangShellLexer(Lexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...

class ElixirLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    KEYWORD: Incomplete
    KEYWORD_OPERATOR: Incomplete
    BUILTIN: Incomplete
    BUILTIN_DECLARATION: Incomplete
    BUILTIN_NAMESPACE: Incomplete
    CONSTANT: Incomplete
    PSEUDO_VAR: Incomplete
    OPERATORS3: Incomplete
    OPERATORS2: Incomplete
    OPERATORS1: Incomplete
    PUNCTUATION: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
    def gen_elixir_sigil_rules(): ...
    op3_re: Incomplete
    op2_re: Incomplete
    op1_re: Incomplete
    ops_re: Incomplete
    punctuation_re: Incomplete
    alnum: str
    name_re: Incomplete
    modname_re: Incomplete
    complex_name_re: Incomplete
    special_atom_re: str
    long_hex_char_re: str
    hex_char_re: str
    escape_char_re: str
    tokens: Incomplete

class ElixirConsoleLexer(Lexer):
    name: str
    aliases: Incomplete
    mimetypes: Incomplete
    def get_tokens_unprocessed(self, text) -> Generator[Incomplete]: ...
