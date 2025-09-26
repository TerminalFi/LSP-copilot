from ..color import Color as Color
from ..distance import DeltaE as DeltaE
from _typeshed import Incomplete
from typing import Any

class DECMC(DeltaE):
    NAME: str
    l: Incomplete
    c: Incomplete
    def __init__(self, l: float = 2, c: float = 1) -> None: ...
    def distance(self, color: Color, sample: Color, l: float | None = None, c: float | None = None, **kwargs: Any) -> float: ...
