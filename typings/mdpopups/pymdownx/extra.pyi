from ..markdown import Extension as Extension
from _typeshed import Incomplete

extra_extensions: Incomplete
extra_extension_configs: Incomplete

class ExtraExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
