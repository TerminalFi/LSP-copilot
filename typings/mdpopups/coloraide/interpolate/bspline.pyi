from ..color import Color as Color
from ..interpolate import Interpolate as Interpolate, Interpolator as Interpolator
from ..types import Vector as Vector
from _typeshed import Incomplete
from typing import Any, Callable, Mapping, Sequence

class InterpolatorBSpline(Interpolator):
    def handle_undefined(self) -> None: ...
    extrapolated: Incomplete
    def adjust_endpoints(self) -> None: ...
    spline: Incomplete
    def setup(self) -> None: ...
    def interpolate(self, point: float, index: int) -> Vector: ...

class BSpline(Interpolate):
    NAME: str
    def interpolator(self, coordinates: list[Vector], channel_names: Sequence[str], create: type['Color'], easings: list[Callable[..., float] | None], stops: dict[int, float], space: str, out_space: str, progress: Mapping[str, Callable[..., float]] | Callable[..., float] | None, premultiplied: bool, extrapolate: bool = False, **kwargs: Any) -> Interpolator: ...
