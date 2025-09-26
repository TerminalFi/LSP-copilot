from .emitter import *
from .serializer import *
from .representer import *
from .resolver import *
from _typeshed import Incomplete

__all__ = ['BaseDumper', 'SafeDumper', 'Dumper']

class BaseDumper(Emitter, Serializer, BaseRepresenter, BaseResolver):
    def __init__(self, stream, default_style: Incomplete | None = None, default_flow_style: bool = False, canonical: Incomplete | None = None, indent: Incomplete | None = None, width: Incomplete | None = None, allow_unicode: Incomplete | None = None, line_break: Incomplete | None = None, encoding: Incomplete | None = None, explicit_start: Incomplete | None = None, explicit_end: Incomplete | None = None, version: Incomplete | None = None, tags: Incomplete | None = None, sort_keys: bool = True) -> None: ...

class SafeDumper(Emitter, Serializer, SafeRepresenter, Resolver):
    def __init__(self, stream, default_style: Incomplete | None = None, default_flow_style: bool = False, canonical: Incomplete | None = None, indent: Incomplete | None = None, width: Incomplete | None = None, allow_unicode: Incomplete | None = None, line_break: Incomplete | None = None, encoding: Incomplete | None = None, explicit_start: Incomplete | None = None, explicit_end: Incomplete | None = None, version: Incomplete | None = None, tags: Incomplete | None = None, sort_keys: bool = True) -> None: ...

class Dumper(Emitter, Serializer, Representer, Resolver):
    def __init__(self, stream, default_style: Incomplete | None = None, default_flow_style: bool = False, canonical: Incomplete | None = None, indent: Incomplete | None = None, width: Incomplete | None = None, allow_unicode: Incomplete | None = None, line_break: Incomplete | None = None, encoding: Incomplete | None = None, explicit_start: Incomplete | None = None, explicit_end: Incomplete | None = None, version: Incomplete | None = None, tags: Incomplete | None = None, sort_keys: bool = True) -> None: ...
