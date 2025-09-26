from . import util as util
from ..markdown import Extension as Extension
from ..markdown.inlinepatterns import InlineProcessor as InlineProcessor
from _typeshed import Incomplete

html_parser: Incomplete
RE_KBD: str
ESCAPE_RE: Incomplete
UNESCAPED_PLUS: Incomplete
ESCAPED_BSLASH: Incomplete
DOUBLE_BSLASH: str

class KeysPattern(InlineProcessor):
    ksep: Incomplete
    strict: Incomplete
    classes: Incomplete
    map: Incomplete
    aliases: Incomplete
    camel: Incomplete
    def __init__(self, pattern, config, md) -> None: ...
    def merge(self, x, y): ...
    def normalize(self, key): ...
    def process_key(self, key): ...
    def handleMatch(self, m, data): ...

class KeysExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
