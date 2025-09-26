from ..formatter import Formatter
from _typeshed import Incomplete

__all__ = ['Terminal256Formatter']

class EscapeSequence:
    fg: Incomplete
    bg: Incomplete
    bold: Incomplete
    underline: Incomplete
    def __init__(self, fg: Incomplete | None = None, bg: Incomplete | None = None, bold: bool = False, underline: bool = False) -> None: ...
    def escape(self, attrs): ...
    def color_string(self): ...
    def reset_string(self): ...

class Terminal256Formatter(Formatter):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    xterm_colors: Incomplete
    best_match: Incomplete
    style_string: Incomplete
    usebold: Incomplete
    useunderline: Incomplete
    def __init__(self, **options) -> None: ...
    encoding: Incomplete
    def format(self, tokensource, outfile): ...
    def format_unencoded(self, tokensource, outfile) -> None: ...
