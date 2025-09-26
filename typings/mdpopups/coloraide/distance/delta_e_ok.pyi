from ..color import Color as Color
from .delta_e_76 import DE76 as DE76
from _typeshed import Incomplete
from typing import Any

class DEOK(DE76):
    NAME: str
    SPACE: str
    scalar: Incomplete
    def __init__(self, scalar: float = 1) -> None: ...
    def distance(self, color: Color, sample: Color, scalar: float | None = None, **kwargs: Any) -> float: ...
