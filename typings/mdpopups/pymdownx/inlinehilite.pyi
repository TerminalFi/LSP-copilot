from ..markdown import Extension as Extension
from ..markdown.inlinepatterns import InlineProcessor as InlineProcessor
from _typeshed import Incomplete

ESCAPED_BSLASH: Incomplete
DOUBLE_BSLASH: str
BACKTICK_CODE_RE: str

class InlineHilitePattern(InlineProcessor):
    config: Incomplete
    md: Incomplete
    formatters: Incomplete
    get_hl_settings: bool
    def __init__(self, pattern, config, md) -> None: ...
    def extend_custom_inline(self, name, formatter) -> None: ...
    style_plain_text: Incomplete
    highlighter: Incomplete
    css_class: Incomplete
    extend_pygments_lang: Incomplete
    guess_lang: Incomplete
    pygments_style: Incomplete
    use_pygments: Incomplete
    noclasses: Incomplete
    language_prefix: Incomplete
    def get_settings(self) -> None: ...
    def highlight_code(self, src: str = '', language: str = '', classname: Incomplete | None = None, md: Incomplete | None = None): ...
    def handle_code(self, lang, src): ...
    def handleMatch(self, m, data): ...

class InlineHiliteExtension(Extension):
    inlinehilite: Incomplete
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
