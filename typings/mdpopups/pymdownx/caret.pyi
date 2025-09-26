from . import util as util
from ..markdown import Extension as Extension
from _typeshed import Incomplete

SMART_CONTENT: str
SMART_MIXED_CONTENT: str
CONTENT: str
CONTENT2: str
INS_SUP: str
INS_SUP2: Incomplete
SUP_INS: Incomplete
INS_SUP3: Incomplete
INS: Incomplete
SUP: Incomplete
SMART_INS_SUP: Incomplete
SMART_INS_SUP2: Incomplete
SMART_SUP_INS: Incomplete
SMART_INS: Incomplete

class CaretProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class CaretSmartProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class CaretSupProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class CaretInsertProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class CaretSmartInsertProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class InsertSupExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
