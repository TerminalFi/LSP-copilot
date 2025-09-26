from _typeshed import Incomplete

__all__ = ['Mark', 'YAMLError', 'MarkedYAMLError']

class Mark:
    name: Incomplete
    index: Incomplete
    line: Incomplete
    column: Incomplete
    buffer: Incomplete
    pointer: Incomplete
    def __init__(self, name, index, line, column, buffer, pointer) -> None: ...
    def get_snippet(self, indent: int = 4, max_length: int = 75): ...

class YAMLError(Exception): ...

class MarkedYAMLError(YAMLError):
    context: Incomplete
    context_mark: Incomplete
    problem: Incomplete
    problem_mark: Incomplete
    note: Incomplete
    def __init__(self, context: Incomplete | None = None, context_mark: Incomplete | None = None, problem: Incomplete | None = None, problem_mark: Incomplete | None = None, note: Incomplete | None = None) -> None: ...
