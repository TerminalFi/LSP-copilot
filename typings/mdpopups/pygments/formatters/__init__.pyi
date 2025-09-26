import types
from ..formatters._mapping import FORMATTERS as FORMATTERS
from ..plugin import find_plugin_formatters as find_plugin_formatters
from ..util import ClassNotFound as ClassNotFound, itervalues as itervalues
from _typeshed import Incomplete
from collections.abc import Generator

def get_all_formatters() -> Generator[Incomplete]: ...
def find_formatter_class(alias): ...
def get_formatter_by_name(_alias, **options): ...
def get_formatter_for_filename(fn, **options): ...

class _automodule(types.ModuleType):
    def __getattr__(self, name): ...

oldmod: Incomplete
newmod: Incomplete
