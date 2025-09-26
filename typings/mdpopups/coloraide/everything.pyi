from .algebra import NaN as NaN
from .color import Color as Base, ColorMatch as ColorMatch
from .interpolate import hint as hint, stop as stop

__all__ = ['ColorAll', 'ColorMatch', 'stop', 'hint', 'NaN']

class ColorAll(Base): ...
