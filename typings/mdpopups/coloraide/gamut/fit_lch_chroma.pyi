from ..algebra import NaN as NaN
from ..color import Color as Color
from ..gamut import Fit as Fit, clip_channels as clip_channels
from typing import Any

class LChChroma(Fit):
    NAME: str
    EPSILON: float
    LIMIT: float
    DE: str
    SPACE: str
    MIN_LIGHTNESS: int
    MAX_LIGHTNESS: int
    def fit(self, color: Color, **kwargs: Any) -> None: ...
