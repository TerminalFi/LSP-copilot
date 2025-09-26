from ..color import Color as Color
from ..contrast import ColorContrast as ColorContrast
from typing import Any

class WCAG21Contrast(ColorContrast):
    NAME: str
    def contrast(self, color1: Color, color2: Color, **kwargs: Any) -> float: ...
