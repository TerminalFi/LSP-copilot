from ..color import Color as Color
from ..types import Plugin as Plugin
from abc import ABCMeta, abstractmethod
from typing import Any

class ColorContrast(Plugin, metaclass=ABCMeta):
    NAME: str
    @abstractmethod
    def contrast(self, color1: Color, color2: Color, **kwargs: Any) -> float: ...

def contrast(name: str | None, color1: Color, color2: Color, **kwargs: Any) -> float: ...
