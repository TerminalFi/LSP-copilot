from . import util as util
from ..markdown import Extension as Extension
from _typeshed import Incomplete

SMART_CONTENT: str
SMART_MIXED_CONTENT: str
CONTENT: str
CONTENT2: str
DEL_SUB: str
DEL_SUB2: Incomplete
SUB_DEL: Incomplete
DEL_SUB3: Incomplete
DEL: Incomplete
SUB: Incomplete
SMART_DEL_SUB: Incomplete
SMART_DEL_SUB2: Incomplete
SMART_SUB_DEL: Incomplete
SMART_DEL: Incomplete

class TildeProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class TildeSmartProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class TildeSubProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class TildeDeleteProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class TildeSmartDeleteProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class DeleteSubExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
