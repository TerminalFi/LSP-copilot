from ..color import Color as Color
from ..types import Plugin as Plugin
from abc import ABCMeta, abstractmethod
from typing import Any

class Filter(Plugin, metaclass=ABCMeta):
    NAME: str
    DEFAULT_SPACE: str
    ALLOWED_SPACES: tuple[str, ...]
    @abstractmethod
    def filter(self, color: Color, amount: float | None, **kwargs: Any) -> None: ...

def filters(color: Color, name: str, amount: float | None = None, space: str | None = None, in_place: bool = False, **kwargs: Any) -> Color: ...
