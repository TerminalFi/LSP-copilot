from . import Extension as Extension
from ..inlinepatterns import InlineProcessor as InlineProcessor
from ..preprocessors import Preprocessor as Preprocessor
from ..util import AtomicString as AtomicString
from _typeshed import Incomplete

ABBR_REF_RE: Incomplete

class AbbrExtension(Extension):
    def extendMarkdown(self, md) -> None: ...

class AbbrPreprocessor(Preprocessor):
    def run(self, lines): ...

class AbbrInlineProcessor(InlineProcessor):
    title: Incomplete
    def __init__(self, pattern, title) -> None: ...
    def handleMatch(self, m, data): ...

def makeExtension(**kwargs): ...
