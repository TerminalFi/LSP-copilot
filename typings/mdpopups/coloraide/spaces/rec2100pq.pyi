from .. import util as util
from ..cat import WHITES as WHITES
from ..types import Vector as Vector
from .srgb import sRGB as sRGB
from _typeshed import Incomplete

class Rec2100PQ(sRGB):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
