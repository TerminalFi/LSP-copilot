from ..color import Color as Color
from ..distance import DeltaE as DeltaE
from _typeshed import Incomplete
from typing import Any

class DE94(DeltaE):
    NAME: str
    kl: Incomplete
    k1: Incomplete
    k2: Incomplete
    def __init__(self, kl: float = 1, k1: float = 0.045, k2: float = 0.015) -> None: ...
    def distance(self, color: Color, sample: Color, kl: float | None = None, k1: float | None = None, k2: float | None = None, **kwargs: Any) -> float: ...
