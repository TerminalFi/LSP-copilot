from _typeshed import Incomplete

class Event:
    start_mark: Incomplete
    end_mark: Incomplete
    def __init__(self, start_mark: Incomplete | None = None, end_mark: Incomplete | None = None) -> None: ...

class NodeEvent(Event):
    anchor: Incomplete
    start_mark: Incomplete
    end_mark: Incomplete
    def __init__(self, anchor, start_mark: Incomplete | None = None, end_mark: Incomplete | None = None) -> None: ...

class CollectionStartEvent(NodeEvent):
    anchor: Incomplete
    tag: Incomplete
    implicit: Incomplete
    start_mark: Incomplete
    end_mark: Incomplete
    flow_style: Incomplete
    def __init__(self, anchor, tag, implicit, start_mark: Incomplete | None = None, end_mark: Incomplete | None = None, flow_style: Incomplete | None = None) -> None: ...

class CollectionEndEvent(Event): ...

class StreamStartEvent(Event):
    start_mark: Incomplete
    end_mark: Incomplete
    encoding: Incomplete
    def __init__(self, start_mark: Incomplete | None = None, end_mark: Incomplete | None = None, encoding: Incomplete | None = None) -> None: ...

class StreamEndEvent(Event): ...

class DocumentStartEvent(Event):
    start_mark: Incomplete
    end_mark: Incomplete
    explicit: Incomplete
    version: Incomplete
    tags: Incomplete
    def __init__(self, start_mark: Incomplete | None = None, end_mark: Incomplete | None = None, explicit: Incomplete | None = None, version: Incomplete | None = None, tags: Incomplete | None = None) -> None: ...

class DocumentEndEvent(Event):
    start_mark: Incomplete
    end_mark: Incomplete
    explicit: Incomplete
    def __init__(self, start_mark: Incomplete | None = None, end_mark: Incomplete | None = None, explicit: Incomplete | None = None) -> None: ...

class AliasEvent(NodeEvent): ...

class ScalarEvent(NodeEvent):
    anchor: Incomplete
    tag: Incomplete
    implicit: Incomplete
    value: Incomplete
    start_mark: Incomplete
    end_mark: Incomplete
    style: Incomplete
    def __init__(self, anchor, tag, implicit, value, start_mark: Incomplete | None = None, end_mark: Incomplete | None = None, style: Incomplete | None = None) -> None: ...

class SequenceStartEvent(CollectionStartEvent): ...
class SequenceEndEvent(CollectionEndEvent): ...
class MappingStartEvent(CollectionStartEvent): ...
class MappingEndEvent(CollectionEndEvent): ...
