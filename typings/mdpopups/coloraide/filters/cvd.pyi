from ..color import Color as Color
from ..filters import Filter as Filter
from ..types import Matrix as Matrix, Vector as Vector
from _typeshed import Incomplete
from typing import Any, Callable

LRGB_TO_LMS: Incomplete
INV_LMS_TO_LRGB: Incomplete
BRETTEL_PROTAN: tuple[Matrix, Matrix, Vector]
BRETTEL_DEUTAN: tuple[Matrix, Matrix, Vector]
BRETTEL_TRITAN: tuple[Matrix, Matrix, Vector]
VIENOT_PROTAN: Incomplete
VIENOT_DEUTAN: Incomplete
VIENOT_TRITAN: Incomplete
MACHADO_PROTAN: dict[int, Matrix]
MACHADO_DEUTAN: dict[int, Matrix]
MACHADO_TRITAN: dict[int, Matrix]

def brettel(color: Color, severity: float, wings: tuple[Matrix, Matrix, Vector]) -> None: ...
def vienot(color: Color, severity: float, transform: Matrix) -> None: ...
def machado(color: Color, severity: float, matrices: dict[int, Matrix]) -> None: ...

class Protan(Filter):
    NAME: str
    ALLOWED_SPACES: Incomplete
    BRETTEL = BRETTEL_PROTAN
    VIENOT = VIENOT_PROTAN
    MACHADO = MACHADO_PROTAN
    severe: Incomplete
    anomalous: Incomplete
    def __init__(self, severe: str = 'vienot', anomalous: str = 'machado') -> None: ...
    def brettel(self, color: Color, severity: float) -> None: ...
    def vienot(self, color: Color, severity: float) -> None: ...
    def machado(self, color: Color, severity: float) -> None: ...
    def select_filter(self, method: str) -> Callable[..., None]: ...
    def get_best_filter(self, method: str | None, max_severity: bool) -> Callable[..., None]: ...
    def filter(self, color: Color, amount: float | None = None, **kwargs: Any) -> None: ...

class Deutan(Protan):
    NAME: str
    BRETTEL = BRETTEL_DEUTAN
    VIENOT = VIENOT_DEUTAN
    MACHADO = MACHADO_DEUTAN

class Tritan(Protan):
    NAME: str
    BRETTEL = BRETTEL_TRITAN
    VIENOT = VIENOT_TRITAN
    MACHADO = MACHADO_TRITAN
    def __init__(self, severe: str = 'brettel', anomalous: str = 'brettel') -> None: ...
