from ..markdown import Extension as Extension
from ..markdown.treeprocessors import Treeprocessor as Treeprocessor
from ..pygments import highlight as highlight
from ..pygments.formatters import find_formatter_class as find_formatter_class
from ..pygments.lexers import get_lexer_by_name as get_lexer_by_name, guess_lexer as guess_lexer
from _typeshed import Incomplete

HtmlFormatter: Incomplete
pygments: bool
CODE_WRAP: str
CODE_WRAP_ON_PRE: str
CLASS_ATTR: str
ID_ATTR: str
DEFAULT_CONFIG: Incomplete
multi_space: Incomplete

def replace_nbsp(m): ...

html_re: Incomplete

class InlineHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile): ...

class BlockHtmlFormatter(HtmlFormatter):
    RE_SPAN_NUMS: Incomplete
    RE_TABLE_NUMS: Incomplete
    pymdownx_inline: Incomplete
    def __init__(self, **options) -> None: ...
    def wrap(self, source, outfile): ...

class SublimeInlineHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile): ...

class SublimeBlockFormatter(BlockHtmlFormatter):
    def wrap(self, source, outfile): ...

class SublimeWrapBlockFormatter(BlockHtmlFormatter):
    def wrap(self, source, outfile): ...

class Highlight:
    guess_lang: Incomplete
    pygments_style: Incomplete
    use_pygments: Incomplete
    noclasses: Incomplete
    linenums: Incomplete
    linenums_style: Incomplete
    linenums_special: Incomplete
    linenums_class: Incomplete
    wrapcode: Incomplete
    language_prefix: Incomplete
    code_attr_on_pre: Incomplete
    sublime_hl: Incomplete
    sublime_wrap: Incomplete
    extend_pygments_lang: Incomplete
    def __init__(self, guess_lang: bool = False, pygments_style: str = 'default', use_pygments: bool = True, noclasses: bool = False, extend_pygments_lang: Incomplete | None = None, linenums: Incomplete | None = None, linenums_special: int = -1, linenums_style: str = 'table', linenums_class: str = 'linenums', wrapcode: bool = True, language_prefix: str = 'language-', code_attr_on_pre: bool = False) -> None: ...
    @classmethod
    def set_sublime_vars(cls, sublime_hl, sublime_wrap, plugin_map) -> None: ...
    def get_extended_language(self, language): ...
    def get_lexer(self, src, language): ...
    def escape(self, txt, code_wrap): ...
    def highlight(self, src, language, css_class: str = 'highlight', hl_lines: Incomplete | None = None, linestart: int = -1, linestep: int = -1, linespecial: int = -1, inline: bool = False, classes: Incomplete | None = None, id_value: str = '', attrs: Incomplete | None = None): ...

class HighlightTreeprocessor(Treeprocessor):
    def __init__(self, md) -> None: ...
    def code_unescape(self, text): ...
    def run(self, root) -> None: ...

class HighlightExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def get_pymdownx_highlight_settings(self): ...
    def get_pymdownx_highlighter(self): ...
    md: Incomplete
    enabled: Incomplete
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
