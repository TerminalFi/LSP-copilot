from _typeshed import Incomplete
from typing import Callable

EPSILON: float
MAX_ITER: int

def cubic_bezier(x1: float, y1: float, x2: float, y2: float) -> Callable[..., float]: ...
def linear(t: float) -> float: ...

ease: Incomplete
ease_in: Incomplete
ease_out: Incomplete
ease_in_out: Incomplete
