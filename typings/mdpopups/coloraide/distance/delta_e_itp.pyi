from ..color import Color as Color
from ..distance import DeltaE as DeltaE
from _typeshed import Incomplete
from typing import Any

class DEITP(DeltaE):
    NAME: str
    scalar: Incomplete
    def __init__(self, scalar: float = 720) -> None: ...
    def distance(self, color: Color, sample: Color, scalar: float | None = None, **kwargs: Any) -> float: ...
