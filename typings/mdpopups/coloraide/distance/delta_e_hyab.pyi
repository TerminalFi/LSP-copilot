from ..color import Color as Color
from ..distance import DeltaE as DeltaE
from ..spaces import Labish as Labish
from _typeshed import Incomplete
from typing import Any

class DEHyAB(DeltaE):
    NAME: str
    space: Incomplete
    def __init__(self, space: str = 'lab-d65') -> None: ...
    def distance(self, color: Color, sample: Color, space: str | None = None, **kwargs: Any) -> float: ...
