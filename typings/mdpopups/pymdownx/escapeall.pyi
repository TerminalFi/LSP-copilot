from . import util as util
from ..markdown import Extension as Extension
from ..markdown.inlinepatterns import InlineProcessor as InlineProcessor, SubstituteTagInlineProcessor as SubstituteTagInlineProcessor
from ..markdown.postprocessors import Postprocessor as Postprocessor
from _typeshed import Incomplete

STX: str
ETX: str
ESCAPE_RE: str
ESCAPE_NO_NL_RE: str
HARDBREAK_RE: str
UNESCAPE_PATTERN: Incomplete

class EscapeAllPattern(InlineProcessor):
    nbsp: Incomplete
    def __init__(self, pattern, nbsp) -> None: ...
    def handleMatch(self, m, data): ...

class EscapeAllPostprocessor(Postprocessor):
    def unescape(self, m): ...
    def run(self, text): ...

class EscapeAllExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
