from .. import oklch as base
from ...color import Color as Color
from ...css import parse as parse, serialize as serialize
from ...types import Vector as Vector
from typing import Any

class OkLCh(base.OkLCh):
    def to_string(self, parent: Color, *, alpha: bool | None = None, precision: int | None = None, fit: str | bool = True, none: bool = False, color: bool = False, percent: bool = False, **kwargs: Any) -> str: ...
    def match(self, string: str, start: int = 0, fullmatch: bool = True) -> tuple[tuple[Vector, float], int] | None: ...
