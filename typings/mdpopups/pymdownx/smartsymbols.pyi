from ..markdown import Extension as Extension, treeprocessors as treeprocessors
from ..markdown.inlinepatterns import HtmlInlineProcessor as HtmlInlineProcessor
from ..markdown.util import Registry as Registry
from _typeshed import Incomplete

RE_TRADE: Incomplete
RE_COPY: Incomplete
RE_REG: Incomplete
RE_PLUSMINUS: Incomplete
RE_NOT_EQUAL: Incomplete
RE_CARE_OF: Incomplete
RE_ORDINAL_NUMBERS: Incomplete
RE_ARROWS: Incomplete
RE_FRACTIONS: Incomplete
REPL: Incomplete
FRAC: Incomplete
ARR: Incomplete

class SmartSymbolsPattern(HtmlInlineProcessor):
    replace: Incomplete
    def __init__(self, pattern, replace, md) -> None: ...
    def handleMatch(self, m, data): ...

class SmartSymbolsExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def add_pattern(self, patterns, md) -> None: ...
    patterns: Incomplete
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
