from ..markdown import Extension as Extension
from ..markdown.postprocessors import Postprocessor as Postprocessor
from _typeshed import Incomplete

RE_TAG_HTML: Incomplete
TAG_BAD_ATTR: str

class StripHtmlPostprocessor(Postprocessor):
    strip_comments: Incomplete
    re_attributes: Incomplete
    def __init__(self, strip_comments, strip_js_on_attributes, strip_attributes, md) -> None: ...
    def repl(self, m): ...
    def run(self, text): ...

class StripHtmlExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
