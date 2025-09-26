from . import Extension as Extension
from ..blockprocessors import BlockProcessor as BlockProcessor
from _typeshed import Incomplete

PIPE_NONE: int
PIPE_LEFT: int
PIPE_RIGHT: int

class TableProcessor(BlockProcessor):
    RE_CODE_PIPES: Incomplete
    RE_END_BORDER: Incomplete
    border: bool
    separator: str
    def __init__(self, parser) -> None: ...
    def test(self, parent, block): ...
    def run(self, parent, blocks) -> None: ...

class TableExtension(Extension):
    def extendMarkdown(self, md) -> None: ...

def makeExtension(**kwargs): ...
