from ..color import Color as Color
from ..distance import DeltaE as DeltaE, distance_euclidean as distance_euclidean
from typing import Any

class DE76(DeltaE):
    NAME: str
    SPACE: str
    def distance(self, color: Color, sample: Color, **kwargs: Any) -> float: ...
