from ..cat import WHITES as WHITES
from ..types import Vector as Vector
from .srgb import gam_srgb as gam_srgb, lin_srgb as lin_srgb, sRGB as sRGB
from _typeshed import Incomplete

class DisplayP3(sRGB):
    BASE: str
    NAME: str
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
