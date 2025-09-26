from .. import srgb as base
from ...color import Color as Color
from ...css import parse as parse, serialize as serialize
from ...types import Vector as Vector
from typing import Any

class sRGB(base.sRGB):
    def to_string(self, parent: Color, *, alpha: bool | None = None, precision: int | None = None, fit: bool | str = True, none: bool = False, color: bool = False, hex: bool = False, names: bool = False, comma: bool = False, upper: bool = False, percent: bool = False, compress: bool = False, **kwargs: Any) -> str: ...
    def match(self, string: str, start: int = 0, fullmatch: bool = True) -> tuple[tuple[Vector, float], int] | None: ...
