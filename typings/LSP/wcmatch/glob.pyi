from typing import Any

BRACE: int
GLOBSTAR: int

def globmatch(filename: Any, patterns: Any, *, flags: int = ..., root_dir: Any | None = ..., limit: Any = ...) -> bool: ...
