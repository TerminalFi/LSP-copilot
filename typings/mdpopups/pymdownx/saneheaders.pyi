from ..markdown import Extension as Extension
from ..markdown.blockprocessors import HashHeaderProcessor as HashHeaderProcessor
from _typeshed import Incomplete

class SaneHeadersProcessor(HashHeaderProcessor):
    RE: Incomplete

class SaneHeadersExtension(Extension):
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
