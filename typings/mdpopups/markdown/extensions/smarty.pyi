from . import Extension as Extension
from ..inlinepatterns import HTML_RE as HTML_RE, HtmlInlineProcessor as HtmlInlineProcessor
from ..treeprocessors import InlineProcessor as InlineProcessor
from ..util import Registry as Registry, deprecated as deprecated
from _typeshed import Incomplete

punctClass: str
endOfWordClass: str
closeClass: str
openingQuotesBase: str
substitutions: Incomplete
singleQuoteStartRe: Incomplete
doubleQuoteStartRe: Incomplete
doubleQuoteSetsRe: str
singleQuoteSetsRe: str
decadeAbbrRe: str
openingDoubleQuotesRegex: Incomplete
closingDoubleQuotesRegex: str
closingDoubleQuotesRegex2: Incomplete
openingSingleQuotesRegex: Incomplete
closingSingleQuotesRegex: Incomplete
closingSingleQuotesRegex2: Incomplete
remainingSingleQuotesRegex: str
remainingDoubleQuotesRegex: str
HTML_STRICT_RE: Incomplete

class SubstituteTextPattern(HtmlInlineProcessor):
    replace: Incomplete
    md: Incomplete
    def __init__(self, pattern, replace, md) -> None: ...
    @property
    def markdown(self): ...
    def handleMatch(self, m, data): ...

class SmartyExtension(Extension):
    config: Incomplete
    substitutions: Incomplete
    def __init__(self, **kwargs) -> None: ...
    def educateDashes(self, md) -> None: ...
    def educateEllipses(self, md) -> None: ...
    def educateAngledQuotes(self, md) -> None: ...
    def educateQuotes(self, md) -> None: ...
    inlinePatterns: Incomplete
    def extendMarkdown(self, md) -> None: ...

def makeExtension(**kwargs): ...
