from . import util as util
from ..markdown import Extension as Extension
from ..markdown.postprocessors import Postprocessor as Postprocessor
from _typeshed import Incomplete

RE_SLASH_WIN_DRIVE: Incomplete
file_types: Incomplete
RE_TAG_HTML: Incomplete
RE_TAG_LINK_ATTR: Incomplete

def repl_path(m, base_path): ...
def repl(m, base_path): ...

class B64Postprocessor(Postprocessor):
    def run(self, text): ...

class B64Extension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
