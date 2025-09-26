from _typeshed import Incomplete

class Token:
    start_mark: Incomplete
    end_mark: Incomplete
    def __init__(self, start_mark, end_mark) -> None: ...

class DirectiveToken(Token):
    id: str
    name: Incomplete
    value: Incomplete
    start_mark: Incomplete
    end_mark: Incomplete
    def __init__(self, name, value, start_mark, end_mark) -> None: ...

class DocumentStartToken(Token):
    id: str

class DocumentEndToken(Token):
    id: str

class StreamStartToken(Token):
    id: str
    start_mark: Incomplete
    end_mark: Incomplete
    encoding: Incomplete
    def __init__(self, start_mark: Incomplete | None = None, end_mark: Incomplete | None = None, encoding: Incomplete | None = None) -> None: ...

class StreamEndToken(Token):
    id: str

class BlockSequenceStartToken(Token):
    id: str

class BlockMappingStartToken(Token):
    id: str

class BlockEndToken(Token):
    id: str

class FlowSequenceStartToken(Token):
    id: str

class FlowMappingStartToken(Token):
    id: str

class FlowSequenceEndToken(Token):
    id: str

class FlowMappingEndToken(Token):
    id: str

class KeyToken(Token):
    id: str

class ValueToken(Token):
    id: str

class BlockEntryToken(Token):
    id: str

class FlowEntryToken(Token):
    id: str

class AliasToken(Token):
    id: str
    value: Incomplete
    start_mark: Incomplete
    end_mark: Incomplete
    def __init__(self, value, start_mark, end_mark) -> None: ...

class AnchorToken(Token):
    id: str
    value: Incomplete
    start_mark: Incomplete
    end_mark: Incomplete
    def __init__(self, value, start_mark, end_mark) -> None: ...

class TagToken(Token):
    id: str
    value: Incomplete
    start_mark: Incomplete
    end_mark: Incomplete
    def __init__(self, value, start_mark, end_mark) -> None: ...

class ScalarToken(Token):
    id: str
    value: Incomplete
    plain: Incomplete
    start_mark: Incomplete
    end_mark: Incomplete
    style: Incomplete
    def __init__(self, value, plain, start_mark, end_mark, style: Incomplete | None = None) -> None: ...
