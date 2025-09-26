from ..color import Color as Color
from ..types import ColorInput as ColorInput, Plugin as Plugin
from abc import ABCMeta, abstractmethod
from typing import Any, Sequence

def closest(color: Color, colors: Sequence[ColorInput], method: str | None = None, **kwargs: Any) -> Color: ...
def distance_euclidean(color: Color, sample: Color, space: str = 'lab-d65') -> float: ...

class DeltaE(Plugin, metaclass=ABCMeta):
    NAME: str
    @abstractmethod
    def distance(self, color: Color, sample: Color, **kwargs: Any) -> float: ...
