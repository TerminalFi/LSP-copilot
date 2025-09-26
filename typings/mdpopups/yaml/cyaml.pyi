from .constructor import *
from .serializer import *
from .representer import *
from .resolver import *
from _typeshed import Incomplete
from _yaml import CEmitter, CParser

__all__ = ['CBaseLoader', 'CSafeLoader', 'CFullLoader', 'CUnsafeLoader', 'CLoader', 'CBaseDumper', 'CSafeDumper', 'CDumper']

class CBaseLoader(CParser, BaseConstructor, BaseResolver):
    def __init__(self, stream) -> None: ...

class CSafeLoader(CParser, SafeConstructor, Resolver):
    def __init__(self, stream) -> None: ...

class CFullLoader(CParser, FullConstructor, Resolver):
    def __init__(self, stream) -> None: ...

class CUnsafeLoader(CParser, UnsafeConstructor, Resolver):
    def __init__(self, stream) -> None: ...

class CLoader(CParser, Constructor, Resolver):
    def __init__(self, stream) -> None: ...

class CBaseDumper(CEmitter, BaseRepresenter, BaseResolver):
    def __init__(self, stream, default_style: Incomplete | None = None, default_flow_style: bool = False, canonical: Incomplete | None = None, indent: Incomplete | None = None, width: Incomplete | None = None, allow_unicode: Incomplete | None = None, line_break: Incomplete | None = None, encoding: Incomplete | None = None, explicit_start: Incomplete | None = None, explicit_end: Incomplete | None = None, version: Incomplete | None = None, tags: Incomplete | None = None, sort_keys: bool = True) -> None: ...

class CSafeDumper(CEmitter, SafeRepresenter, Resolver):
    def __init__(self, stream, default_style: Incomplete | None = None, default_flow_style: bool = False, canonical: Incomplete | None = None, indent: Incomplete | None = None, width: Incomplete | None = None, allow_unicode: Incomplete | None = None, line_break: Incomplete | None = None, encoding: Incomplete | None = None, explicit_start: Incomplete | None = None, explicit_end: Incomplete | None = None, version: Incomplete | None = None, tags: Incomplete | None = None, sort_keys: bool = True) -> None: ...

class CDumper(CEmitter, Serializer, Representer, Resolver):
    def __init__(self, stream, default_style: Incomplete | None = None, default_flow_style: bool = False, canonical: Incomplete | None = None, indent: Incomplete | None = None, width: Incomplete | None = None, allow_unicode: Incomplete | None = None, line_break: Incomplete | None = None, encoding: Incomplete | None = None, explicit_start: Incomplete | None = None, explicit_end: Incomplete | None = None, version: Incomplete | None = None, tags: Incomplete | None = None, sort_keys: bool = True) -> None: ...
