from ..channels import FLG_ANGLE as FLG_ANGLE
from ..color import Color as Color
from ..types import Plugin as Plugin
from abc import ABCMeta, abstractmethod
from typing import Any

def clip_channels(color: Color) -> None: ...
def verify(color: Color, tolerance: float) -> bool: ...

class Fit(Plugin, metaclass=ABCMeta):
    NAME: str
    @abstractmethod
    def fit(self, color: Color, **kwargs: Any) -> None: ...
