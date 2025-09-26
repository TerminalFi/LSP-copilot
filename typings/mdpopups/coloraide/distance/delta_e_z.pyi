from ..color import Color as Color
from ..distance import DeltaE as DeltaE
from typing import Any

class DEZ(DeltaE):
    NAME: str
    def distance(self, color: Color, sample: Color, **kwargs: Any) -> float: ...
