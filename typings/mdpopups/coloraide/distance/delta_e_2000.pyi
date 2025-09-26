from ..color import Color as Color
from ..distance import DeltaE as DeltaE
from _typeshed import Incomplete
from typing import Any

class DE2000(DeltaE):
    NAME: str
    LAB: str
    G_CONST: Incomplete
    @classmethod
    def distance(cls, color: Color, sample: Color, kl: float = 1, kc: float = 1, kh: float = 1, **kwargs: Any) -> float: ...
