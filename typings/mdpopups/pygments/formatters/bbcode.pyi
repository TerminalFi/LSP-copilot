from ..formatter import Formatter
from _typeshed import Incomplete

__all__ = ['BBCodeFormatter']

class BBCodeFormatter(Formatter):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    styles: Incomplete
    def __init__(self, **options) -> None: ...
    def format_unencoded(self, tokensource, outfile) -> None: ...
