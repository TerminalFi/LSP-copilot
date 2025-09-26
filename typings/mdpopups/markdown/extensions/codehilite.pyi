from . import Extension as Extension
from ...pygments import highlight as highlight
from ...pygments.formatters import get_formatter_by_name as get_formatter_by_name
from ...pygments.lexers import get_lexer_by_name as get_lexer_by_name, guess_lexer as guess_lexer
from ..treeprocessors import Treeprocessor as Treeprocessor
from _typeshed import Incomplete

pygments: bool

def parse_hl_lines(expr): ...

class CodeHilite:
    src: Incomplete
    lang: Incomplete
    linenums: Incomplete
    guess_lang: Incomplete
    css_class: Incomplete
    style: Incomplete
    noclasses: Incomplete
    tab_length: Incomplete
    hl_lines: Incomplete
    use_pygments: Incomplete
    def __init__(self, src: Incomplete | None = None, linenums: Incomplete | None = None, guess_lang: bool = True, css_class: str = 'codehilite', lang: Incomplete | None = None, style: str = 'default', noclasses: bool = False, tab_length: int = 4, hl_lines: Incomplete | None = None, use_pygments: bool = True) -> None: ...
    def hilite(self): ...

class HiliteTreeprocessor(Treeprocessor):
    def code_unescape(self, text): ...
    def run(self, root) -> None: ...

class CodeHiliteExtension(Extension):
    config: Incomplete
    def __init__(self, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(**kwargs): ...
