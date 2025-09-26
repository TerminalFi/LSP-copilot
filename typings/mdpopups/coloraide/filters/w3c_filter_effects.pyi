from ..color import Color as Color
from ..filters import Filter as Filter
from _typeshed import Incomplete
from typing import Any

def linear_transfer(value: float, slope: float = 1.0, intercept: float = 0.0) -> float: ...

class Sepia(Filter):
    NAME: str
    ALLOWED_SPACES: Incomplete
    def filter(self, color: Color, amount: float | None, **kwargs: Any) -> None: ...

class Grayscale(Filter):
    NAME: str
    ALLOWED_SPACES: Incomplete
    def filter(self, color: Color, amount: float | None, **kwargs: Any) -> None: ...

class Saturate(Filter):
    NAME: str
    ALLOWED_SPACES: Incomplete
    def filter(self, color: Color, amount: float | None, **kwargs: Any) -> None: ...

class Invert(Filter):
    NAME: str
    ALLOWED_SPACES: Incomplete
    def filter(self, color: Color, amount: float | None, **kwargs: Any) -> None: ...

class Opacity(Filter):
    NAME: str
    ALLOWED_SPACES: Incomplete
    def filter(self, color: Color, amount: float | None, **kwargs: Any) -> None: ...

class Brightness(Filter):
    NAME: str
    ALLOWED_SPACES: Incomplete
    def filter(self, color: Color, amount: float | None, **kwargs: Any) -> None: ...

class Contrast(Filter):
    NAME: str
    ALLOWED_SPACES: Incomplete
    def filter(self, color: Color, amount: float | None, **kwargs: Any) -> None: ...

class HueRotate(Filter):
    NAME: str
    ALLOWED_SPACES: Incomplete
    def filter(self, color: Color, amount: float | None, **kwargs: Any) -> None: ...
