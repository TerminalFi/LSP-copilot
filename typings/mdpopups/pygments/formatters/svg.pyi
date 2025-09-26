from ..formatter import Formatter
from _typeshed import Incomplete

__all__ = ['SvgFormatter']

class SvgFormatter(Formatter):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    nowrap: Incomplete
    fontfamily: Incomplete
    fontsize: Incomplete
    xoffset: Incomplete
    yoffset: Incomplete
    ystep: Incomplete
    spacehack: Incomplete
    def __init__(self, **options) -> None: ...
    def format_unencoded(self, tokensource, outfile) -> None: ...
