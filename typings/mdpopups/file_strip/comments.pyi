from _typeshed import Incomplete

LINE_PRESERVE: Incomplete
CPP_PATTERN: Incomplete
PY_PATTERN: Incomplete

class CommentException(Exception):
    value: Incomplete
    def __init__(self, value) -> None: ...

class Comments:
    styles: Incomplete
    preserve_lines: Incomplete
    call: Incomplete
    def __init__(self, style: Incomplete | None = None, preserve_lines: bool = False) -> None: ...
    @classmethod
    def add_style(cls, style, fn) -> None: ...
    def strip(self, text): ...
