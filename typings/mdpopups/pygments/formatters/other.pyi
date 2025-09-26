from ..formatter import Formatter
from _typeshed import Incomplete

__all__ = ['NullFormatter', 'RawTokenFormatter', 'TestcaseFormatter']

class NullFormatter(Formatter):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    def format(self, tokensource, outfile) -> None: ...

class RawTokenFormatter(Formatter):
    name: str
    aliases: Incomplete
    filenames: Incomplete
    unicodeoutput: bool
    encoding: str
    compress: Incomplete
    error_color: Incomplete
    def __init__(self, **options) -> None: ...
    def format(self, tokensource, outfile) -> None: ...

class TestcaseFormatter(Formatter):
    name: str
    aliases: Incomplete
    def __init__(self, **options) -> None: ...
    def format(self, tokensource, outfile) -> None: ...
