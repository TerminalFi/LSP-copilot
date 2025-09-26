from ..formatter import Formatter
from _typeshed import Incomplete

__all__ = ['RtfFormatter']

class RtfFormatter(Formatter):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    fontface: Incomplete
    fontsize: Incomplete
    def __init__(self, **options) -> None: ...
    def format_unencoded(self, tokensource, outfile) -> None: ...
