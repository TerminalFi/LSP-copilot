from ..color import Color as Color
from ..interpolate import Interpolate as Interpolate, Interpolator as Interpolator
from ..types import Vector as Vector
from .bspline import InterpolatorBSpline as InterpolatorBSpline
from _typeshed import Incomplete
from typing import Any, Callable, Mapping, Sequence

class InterpolatorCatmullRom(InterpolatorBSpline):
    spline: Incomplete
    def setup(self) -> None: ...

class CatmullRom(Interpolate):
    NAME: str
    def interpolator(self, coordinates: list[Vector], channel_names: Sequence[str], create: type['Color'], easings: list[Callable[..., float] | None], stops: dict[int, float], space: str, out_space: str, progress: Mapping[str, Callable[..., float]] | Callable[..., float] | None, premultiplied: bool, extrapolate: bool = False, **kwargs: Any) -> Interpolator: ...
