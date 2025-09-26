from . import Extension as Extension
from ..blockprocessors import BlockProcessor as BlockProcessor
from _typeshed import Incomplete

class AdmonitionExtension(Extension):
    def extendMarkdown(self, md) -> None: ...

class AdmonitionProcessor(BlockProcessor):
    CLASSNAME: str
    CLASSNAME_TITLE: str
    RE: Incomplete
    RE_SPACES: Incomplete
    def test(self, parent, block): ...
    def run(self, parent, blocks) -> None: ...
    def get_class_and_title(self, match): ...

def makeExtension(**kwargs): ...
