from ..color import Color
from ..types import ColorInput, Plugin, Vector
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Mapping, Sequence

__all__ = ['stop', 'hint', 'get_interpolator']

class stop:
    color: Incomplete
    stop: Incomplete
    def __init__(self, color: ColorInput, value: float) -> None: ...

def hint(mid: float) -> Callable[..., float]: ...

class Interpolator(metaclass=ABCMeta):
    start: Incomplete
    end: Incomplete
    stops: Incomplete
    easings: Incomplete
    coordinates: Incomplete
    length: Incomplete
    channel_names: Incomplete
    create: Incomplete
    progress: Incomplete
    space: Incomplete
    out_space: Incomplete
    extrapolate: Incomplete
    current_easing: Incomplete
    hue_index: Incomplete
    premultiplied: Incomplete
    def __init__(self, coordinates: list[Vector], channel_names: Sequence[str], create: type['Color'], easings: list[Callable[..., float] | None], stops: dict[int, float], space: str, out_space: str, progress: Callable[..., float] | Mapping[str, Callable[..., float]] | None, premultiplied: bool, extrapolate: bool = False, **kwargs: Any) -> None: ...
    def setup(self) -> None: ...
    @abstractmethod
    def interpolate(self, point: float, index: int) -> Vector: ...
    def steps(self, steps: int = 2, max_steps: int = 1000, max_delta_e: float = 0, delta_e: str | None = None) -> list['Color']: ...
    def premultiply(self, coords: Vector, alpha: float | None = None) -> None: ...
    def postdivide(self, coords: Vector) -> None: ...
    def begin(self, point: float, first: float, last: float, index: int) -> Color: ...
    def ease(self, t: float, channel_index: int) -> float: ...
    def __call__(self, point: float) -> Color: ...

class Interpolate(Plugin, metaclass=ABCMeta):
    NAME: str
    @abstractmethod
    def interpolator(self, coordinates: list[Vector], channel_names: Sequence[str], create: type['Color'], easings: list[Callable[..., float] | None], stops: dict[int, float], space: str, out_space: str, progress: Mapping[str, Callable[..., float]] | Callable[..., float] | None, premultiplied: bool, **kwargs: Any) -> Interpolator: ...

# Names in __all__ with no definition:
#   get_interpolator
