from ..formatter import Formatter
from _typeshed import Incomplete

__all__ = ['HtmlFormatter']

class HtmlFormatter(Formatter):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    title: Incomplete
    nowrap: Incomplete
    noclasses: Incomplete
    classprefix: Incomplete
    cssclass: Incomplete
    cssstyles: Incomplete
    prestyles: Incomplete
    cssfile: Incomplete
    noclobber_cssfile: Incomplete
    tagsfile: Incomplete
    tagurlformat: Incomplete
    linenos: int
    linenostart: Incomplete
    linenostep: Incomplete
    linenospecial: Incomplete
    nobackground: Incomplete
    lineseparator: Incomplete
    lineanchors: Incomplete
    linespans: Incomplete
    anchorlinenos: Incomplete
    hl_lines: Incomplete
    def __init__(self, **options) -> None: ...
    def get_style_defs(self, arg: Incomplete | None = None): ...
    def wrap(self, source, outfile): ...
    def format_unencoded(self, tokensource, outfile) -> None: ...
