from .pygments import highlight as highlight
from .pygments.formatters import find_formatter_class as find_formatter_class
from .pygments.lexers import get_lexer_by_name as get_lexer_by_name, guess_lexer as guess_lexer
from _typeshed import Incomplete

HtmlFormatter: Incomplete
pygments: bool
html_re: Incomplete
multi_space: Incomplete

def replace_nbsp(m): ...

class SublimeWrapBlockFormatter(HtmlFormatter):
    def wrap(self, source, outfile): ...

class SublimeBlockFormatter(HtmlFormatter):
    def wrap(self, source, outfile): ...

class SublimeInlineHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile): ...

def syntax_hl(src, lang: Incomplete | None = None, guess_lang: bool = False, inline: bool = False, code_wrap: bool = False): ...
