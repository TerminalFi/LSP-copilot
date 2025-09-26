from . import Extension as Extension
from ..inlinepatterns import SubstituteTagInlineProcessor as SubstituteTagInlineProcessor

BR_RE: str

class Nl2BrExtension(Extension):
    def extendMarkdown(self, md) -> None: ...

def makeExtension(**kwargs): ...
