from . import util as util
from ..markdown import Extension as Extension
from ..markdown.inlinepatterns import InlineProcessor as InlineProcessor
from _typeshed import Incomplete

RE_EMOJI: str
SUPPORTED_INDEXES: Incomplete
UNICODE_VARIATION_SELECTOR_16: str
EMOJIONE_SVG_CDN: str
EMOJIONE_PNG_CDN: str
TWEMOJI_SVG_CDN: str
TWEMOJI_PNG_CDN: str
GITHUB_UNICODE_CDN: str
GITHUB_CDN: str
NO_TITLE: str
LONG_TITLE: str
SHORT_TITLE: str
VALID_TITLE: Incomplete
UNICODE_ENTITY: str
UNICODE_ALT: Incomplete
LEGACY_ARG_COUNT: int
MSG_INDEX_WARN: str

def add_attriubtes(options, attributes) -> None: ...
def emojione(options, md): ...
def gemoji(options, md): ...
def twemoji(options, md): ...
def to_png(index, shortname, alias, uc, alt, title, category, options, md): ...
def to_svg(index, shortname, alias, uc, alt, title, category, options, md): ...
def to_png_sprite(index, shortname, alias, uc, alt, title, category, options, md): ...
def to_svg_sprite(index, shortname, alias, uc, alt, title, category, options, md): ...
def to_alt(index, shortname, alias, uc, alt, title, category, options, md): ...

class EmojiPattern(InlineProcessor):
    options: Incomplete
    unicode_alt: Incomplete
    encoded_alt: Incomplete
    remove_var_sel: Incomplete
    title: Incomplete
    generator: Incomplete
    def __init__(self, pattern, config, md) -> None: ...
    def handleMatch(self, m, data): ...

class EmojiExtension(Extension):
    config: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def extendMarkdown(self, md) -> None: ...

def makeExtension(*args, **kwargs): ...
