from . import util as util
from ..markdown import Extension as Extension
from _typeshed import Incomplete

SMART_UNDER_CONTENT: str
SMART_STAR_CONTENT: str
SMART_UNDER_MIXED_CONTENT: str
SMART_STAR_MIXED_CONTENT: str
UNDER_CONTENT: str
UNDER_CONTENT2: str
STAR_CONTENT: str
STAR_CONTENT2: str
STAR_STRONG_EM: str
UNDER_STRONG_EM: str
STAR_STRONG_EM2: Incomplete
UNDER_STRONG_EM2: Incomplete
STAR_EM_STRONG: Incomplete
STAR_STRONG_EM3: Incomplete
UNDER_EM_STRONG: Incomplete
UNDER_STRONG_EM3: Incomplete
STAR_STRONG: Incomplete
UNDER_STRONG: Incomplete
STAR_EM: Incomplete
UNDER_EM: Incomplete
SMART_UNDER_STRONG_EM: Incomplete
SMART_UNDER_STRONG_EM2: Incomplete
SMART_UNDER_EM_STRONG: Incomplete
SMART_UNDER_STRONG: Incomplete
SMART_UNDER_EM: Incomplete
SMART_STAR_STRONG_EM: Incomplete
SMART_STAR_STRONG_EM2: Incomplete
SMART_STAR_EM_STRONG: Incomplete
SMART_STAR_STRONG: Incomplete
SMART_STAR_EM: Incomplete

class AsteriskProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class SmartAsteriskProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class UnderscoreProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class SmartUnderscoreProcessor(util.PatternSequenceProcessor):
    PATTERNS: Incomplete

class BetterEmExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...
    def make_better(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
