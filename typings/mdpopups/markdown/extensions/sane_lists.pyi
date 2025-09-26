from . import Extension as Extension
from ..blockprocessors import OListProcessor as OListProcessor, UListProcessor as UListProcessor
from _typeshed import Incomplete

class SaneOListProcessor(OListProcessor):
    SIBLING_TAGS: Incomplete
    LAZY_OL: bool
    CHILD_RE: Incomplete
    def __init__(self, parser) -> None: ...

class SaneUListProcessor(UListProcessor):
    SIBLING_TAGS: Incomplete
    CHILD_RE: Incomplete
    def __init__(self, parser) -> None: ...

class SaneListExtension(Extension):
    def extendMarkdown(self, md) -> None: ...

def makeExtension(**kwargs): ...
