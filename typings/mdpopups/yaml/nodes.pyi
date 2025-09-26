from _typeshed import Incomplete

class Node:
    tag: Incomplete
    value: Incomplete
    start_mark: Incomplete
    end_mark: Incomplete
    def __init__(self, tag, value, start_mark, end_mark) -> None: ...

class ScalarNode(Node):
    id: str
    tag: Incomplete
    value: Incomplete
    start_mark: Incomplete
    end_mark: Incomplete
    style: Incomplete
    def __init__(self, tag, value, start_mark: Incomplete | None = None, end_mark: Incomplete | None = None, style: Incomplete | None = None) -> None: ...

class CollectionNode(Node):
    tag: Incomplete
    value: Incomplete
    start_mark: Incomplete
    end_mark: Incomplete
    flow_style: Incomplete
    def __init__(self, tag, value, start_mark: Incomplete | None = None, end_mark: Incomplete | None = None, flow_style: Incomplete | None = None) -> None: ...

class SequenceNode(CollectionNode):
    id: str

class MappingNode(CollectionNode):
    id: str
