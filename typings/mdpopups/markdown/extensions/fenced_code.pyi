from . import Extension as Extension
from ..preprocessors import Preprocessor as Preprocessor
from .codehilite import CodeHilite as CodeHilite, CodeHiliteExtension as CodeHiliteExtension, parse_hl_lines as parse_hl_lines
from _typeshed import Incomplete

class FencedCodeExtension(Extension):
    def extendMarkdown(self, md) -> None: ...

class FencedBlockPreprocessor(Preprocessor):
    FENCED_BLOCK_RE: Incomplete
    CODE_WRAP: str
    LANG_TAG: str
    checked_for_codehilite: bool
    codehilite_conf: Incomplete
    def __init__(self, md) -> None: ...
    def run(self, lines): ...

def makeExtension(**kwargs): ...
