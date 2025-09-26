from . import util as util
from ..markdown import Extension as Extension
from _typeshed import Incomplete

SMART_CONTENT: str
CONTENT: str
MARK: Incomplete
SMART_MARK: Incomplete

class MarkProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class MarkSmartProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class MarkExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
