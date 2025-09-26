from _typeshed import Incomplete

__all__ = ['Formatter']

class Formatter:
    name: Incomplete
    aliases: Incomplete
    filenames: Incomplete
    unicodeoutput: bool
    style: Incomplete
    full: Incomplete
    title: Incomplete
    encoding: Incomplete
    options: Incomplete
    def __init__(self, **options) -> None: ...
    def get_style_defs(self, arg: str = ''): ...
    def format(self, tokensource, outfile): ...
