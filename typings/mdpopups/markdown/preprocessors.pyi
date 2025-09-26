from . import util as util
from _typeshed import Incomplete

def build_preprocessors(md, **kwargs): ...

class Preprocessor(util.Processor):
    def run(self, lines) -> None: ...

class NormalizeWhitespace(Preprocessor):
    def run(self, lines): ...

class HtmlBlockPreprocessor(Preprocessor):
    right_tag_patterns: Incomplete
    attrs_pattern: str
    left_tag_pattern: Incomplete
    attrs_re: Incomplete
    left_tag_re: Incomplete
    markdown_in_raw: bool
    def run(self, lines): ...

class ReferencePreprocessor(Preprocessor):
    TITLE: str
    RE: Incomplete
    TITLE_RE: Incomplete
    def run(self, lines): ...
