from ..lexer import ExtendedRegexLexer, LexerContext, RegexLexer
from _typeshed import Incomplete

__all__ = ['YamlLexer', 'JsonLexer', 'JsonLdLexer']

class YamlLexerContext(LexerContext):
    indent_stack: Incomplete
    indent: int
    next_indent: int
    block_scalar_indent: Incomplete
    def __init__(self, *args, **kwds) -> None: ...

class YamlLexer(ExtendedRegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    def something(token_class): ...
    def reset_indent(token_class): ...
    def save_indent(token_class, start: bool = False): ...
    def set_indent(token_class, implicit: bool = False): ...
    def set_block_scalar_indent(token_class): ...
    def parse_block_scalar_empty_line(indent_token_class, content_token_class): ...
    def parse_block_scalar_indent(token_class): ...
    def parse_plain_scalar_indent(token_class): ...
    tokens: Incomplete
    def get_tokens_unprocessed(self, text: Incomplete | None = None, context: Incomplete | None = None): ...

class JsonLexer(RegexLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    flags: Incomplete
    int_part: str
    frac_part: str
    exp_part: str
    tokens: Incomplete

class JsonLdLexer(JsonLexer):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    mimetypes: Incomplete
    tokens: Incomplete
