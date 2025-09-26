from ._compat import implements_iterator as implements_iterator, intern as intern, iteritems as iteritems, text_type as text_type
from .exceptions import TemplateSyntaxError as TemplateSyntaxError
from .utils import LRUCache as LRUCache
from _typeshed import Incomplete
from collections.abc import Generator

whitespace_re: Incomplete
string_re: Incomplete
integer_re: Incomplete
name_re: Incomplete
check_ident: bool
float_re: Incomplete
newline_re: Incomplete
TOKEN_ADD: Incomplete
TOKEN_ASSIGN: Incomplete
TOKEN_COLON: Incomplete
TOKEN_COMMA: Incomplete
TOKEN_DIV: Incomplete
TOKEN_DOT: Incomplete
TOKEN_EQ: Incomplete
TOKEN_FLOORDIV: Incomplete
TOKEN_GT: Incomplete
TOKEN_GTEQ: Incomplete
TOKEN_LBRACE: Incomplete
TOKEN_LBRACKET: Incomplete
TOKEN_LPAREN: Incomplete
TOKEN_LT: Incomplete
TOKEN_LTEQ: Incomplete
TOKEN_MOD: Incomplete
TOKEN_MUL: Incomplete
TOKEN_NE: Incomplete
TOKEN_PIPE: Incomplete
TOKEN_POW: Incomplete
TOKEN_RBRACE: Incomplete
TOKEN_RBRACKET: Incomplete
TOKEN_RPAREN: Incomplete
TOKEN_SEMICOLON: Incomplete
TOKEN_SUB: Incomplete
TOKEN_TILDE: Incomplete
TOKEN_WHITESPACE: Incomplete
TOKEN_FLOAT: Incomplete
TOKEN_INTEGER: Incomplete
TOKEN_NAME: Incomplete
TOKEN_STRING: Incomplete
TOKEN_OPERATOR: Incomplete
TOKEN_BLOCK_BEGIN: Incomplete
TOKEN_BLOCK_END: Incomplete
TOKEN_VARIABLE_BEGIN: Incomplete
TOKEN_VARIABLE_END: Incomplete
TOKEN_RAW_BEGIN: Incomplete
TOKEN_RAW_END: Incomplete
TOKEN_COMMENT_BEGIN: Incomplete
TOKEN_COMMENT_END: Incomplete
TOKEN_COMMENT: Incomplete
TOKEN_LINESTATEMENT_BEGIN: Incomplete
TOKEN_LINESTATEMENT_END: Incomplete
TOKEN_LINECOMMENT_BEGIN: Incomplete
TOKEN_LINECOMMENT_END: Incomplete
TOKEN_LINECOMMENT: Incomplete
TOKEN_DATA: Incomplete
TOKEN_INITIAL: Incomplete
TOKEN_EOF: Incomplete
operators: Incomplete
reverse_operators: Incomplete
operator_re: Incomplete
ignored_tokens: Incomplete
ignore_if_empty: Incomplete

def describe_token(token): ...
def describe_token_expr(expr): ...
def count_newlines(value): ...
def compile_rules(environment): ...

class Failure:
    message: Incomplete
    error_class: Incomplete
    def __init__(self, message, cls=...) -> None: ...
    def __call__(self, lineno, filename) -> None: ...

class Token(tuple):
    lineno: Incomplete
    type: Incomplete
    value: Incomplete
    def __new__(cls, lineno, type, value): ...
    def test(self, expr): ...
    def test_any(self, *iterable): ...

class TokenStreamIterator:
    stream: Incomplete
    def __init__(self, stream) -> None: ...
    def __iter__(self): ...
    def __next__(self): ...

class TokenStream:
    name: Incomplete
    filename: Incomplete
    closed: bool
    current: Incomplete
    def __init__(self, generator, name, filename) -> None: ...
    def __iter__(self): ...
    def __bool__(self) -> bool: ...
    __nonzero__ = __bool__
    eos: Incomplete
    def push(self, token) -> None: ...
    def look(self): ...
    def skip(self, n: int = 1) -> None: ...
    def next_if(self, expr): ...
    def skip_if(self, expr): ...
    def __next__(self): ...
    def close(self) -> None: ...
    def expect(self, expr): ...

def get_lexer(environment): ...

class Lexer:
    newline_sequence: Incomplete
    keep_trailing_newline: Incomplete
    rules: Incomplete
    def __init__(self, environment) -> None: ...
    def tokenize(self, source, name: Incomplete | None = None, filename: Incomplete | None = None, state: Incomplete | None = None): ...
    def wrap(self, stream, name: Incomplete | None = None, filename: Incomplete | None = None) -> Generator[Incomplete]: ...
    def tokeniter(self, source, name, filename: Incomplete | None = None, state: Incomplete | None = None) -> Generator[Incomplete]: ...
