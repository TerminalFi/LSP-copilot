from ..markdown import Extension as Extension
from ..markdown.preprocessors import Preprocessor as Preprocessor
from ..markdown.util import ETX as ETX, STX as STX
from _typeshed import Incomplete

SOH: str
EOT: str

class PreNormalizePreprocessor(Preprocessor):
    def run(self, lines): ...

class PostNormalizePreprocessor(Preprocessor):
    def run(self, lines): ...

class BypassNormExtension(Extension):
    inlinehilite: Incomplete
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
