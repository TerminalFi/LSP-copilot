from . import Extension as Extension
from ..preprocessors import Preprocessor as Preprocessor
from _typeshed import Incomplete

log: Incomplete
META_RE: Incomplete
META_MORE_RE: Incomplete
BEGIN_RE: Incomplete
END_RE: Incomplete

class MetaExtension(Extension):
    md: Incomplete
    def extendMarkdown(self, md) -> None: ...
    def reset(self) -> None: ...

class MetaPreprocessor(Preprocessor):
    def run(self, lines): ...

def makeExtension(**kwargs): ...
