from ..extensions import Extension as Extension
from ..treeprocessors import Treeprocessor as Treeprocessor, isString as isString
from _typeshed import Incomplete

ATTR_RE: Incomplete

class LegacyAttrs(Treeprocessor):
    def run(self, doc) -> None: ...
    def handleAttributes(self, el, txt): ...

class LegacyAttrExtension(Extension):
    def extendMarkdown(self, md) -> None: ...

def makeExtension(**kwargs): ...
