from .reader import *
from .scanner import *
from .parser import *
from .composer import *
from .constructor import *
from .resolver import *

__all__ = ['BaseLoader', 'FullLoader', 'SafeLoader', 'Loader', 'UnsafeLoader']

class BaseLoader(Reader, Scanner, Parser, Composer, BaseConstructor, BaseResolver):
    def __init__(self, stream) -> None: ...

class FullLoader(Reader, Scanner, Parser, Composer, FullConstructor, Resolver):
    def __init__(self, stream) -> None: ...

class SafeLoader(Reader, Scanner, Parser, Composer, SafeConstructor, Resolver):
    def __init__(self, stream) -> None: ...

class Loader(Reader, Scanner, Parser, Composer, Constructor, Resolver):
    def __init__(self, stream) -> None: ...

class UnsafeLoader(Reader, Scanner, Parser, Composer, Constructor, Resolver):
    def __init__(self, stream) -> None: ...
