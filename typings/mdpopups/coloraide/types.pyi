from .color import Color as Color
from _typeshed import Incomplete
from typing import Sequence, TypeVar

ColorInput: Incomplete
Vector = list[float]
Matrix = list[Vector]
Array = Matrix | Vector
VectorLike = Sequence[float]
MatrixLike = Sequence[VectorLike]
ArrayLike = VectorLike | MatrixLike
SupportsFloatOrInt = TypeVar('SupportsFloatOrInt', float, int)

class Plugin:
    NAME: str
