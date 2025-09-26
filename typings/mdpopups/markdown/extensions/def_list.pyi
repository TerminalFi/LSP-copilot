from . import Extension as Extension
from ..blockprocessors import BlockProcessor as BlockProcessor, ListIndentProcessor as ListIndentProcessor
from _typeshed import Incomplete

class DefListProcessor(BlockProcessor):
    RE: Incomplete
    NO_INDENT_RE: Incomplete
    def test(self, parent, block): ...
    def run(self, parent, blocks): ...

class DefListIndentProcessor(ListIndentProcessor):
    ITEM_TYPES: Incomplete
    LIST_TYPES: Incomplete
    def create_item(self, parent, block) -> None: ...

class DefListExtension(Extension):
    def extendMarkdown(self, md) -> None: ...

def makeExtension(**kwargs): ...
