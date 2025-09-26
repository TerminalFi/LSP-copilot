from .error import YAMLError
from _typeshed import Incomplete

__all__ = ['Reader', 'ReaderError']

class ReaderError(YAMLError):
    name: Incomplete
    character: Incomplete
    position: Incomplete
    encoding: Incomplete
    reason: Incomplete
    def __init__(self, name, position, character, encoding, reason) -> None: ...

class Reader:
    name: Incomplete
    stream: Incomplete
    stream_pointer: int
    eof: bool
    buffer: str
    pointer: int
    raw_buffer: Incomplete
    raw_decode: Incomplete
    encoding: Incomplete
    index: int
    line: int
    column: int
    def __init__(self, stream) -> None: ...
    def peek(self, index: int = 0): ...
    def prefix(self, length: int = 1): ...
    def forward(self, length: int = 1) -> None: ...
    def get_mark(self): ...
    def determine_encoding(self) -> None: ...
    NON_PRINTABLE: Incomplete
    def check_printable(self, data) -> None: ...
    def update(self, length) -> None: ...
    def update_raw(self, size: int = 4096) -> None: ...
