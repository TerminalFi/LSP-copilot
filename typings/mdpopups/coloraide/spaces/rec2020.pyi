from ..cat import WHITES as WHITES
from ..types import Vector as Vector
from .srgb import sRGB as sRGB
from _typeshed import Incomplete

ALPHA: float
BETA: float
BETA45: Incomplete

def lin_2020(rgb: Vector) -> Vector: ...
def gam_2020(rgb: Vector) -> Vector: ...

class Rec2020(sRGB):
    BASE: str
    NAME: str
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
