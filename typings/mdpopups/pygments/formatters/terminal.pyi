from ..formatter import Formatter
from _typeshed import Incomplete

__all__ = ['TerminalFormatter']

class TerminalFormatter(Formatter):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    darkbg: Incomplete
    colorscheme: Incomplete
    linenos: Incomplete
    def __init__(self, **options) -> None: ...
    encoding: Incomplete
    def format(self, tokensource, outfile): ...
    def format_unencoded(self, tokensource, outfile) -> None: ...
