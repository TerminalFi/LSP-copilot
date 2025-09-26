from . import Extension as Extension
from _typeshed import Incomplete

extensions: Incomplete

class ExtraExtension(Extension):
    config: Incomplete
    def __init__(self, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(**kwargs): ...
