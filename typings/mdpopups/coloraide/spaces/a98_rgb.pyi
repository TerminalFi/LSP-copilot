from ..cat import WHITES as WHITES
from ..types import Vector as Vector
from .srgb import sRGB as sRGB
from _typeshed import Incomplete

def lin_a98rgb(rgb: Vector) -> Vector: ...
def gam_a98rgb(rgb: Vector) -> Vector: ...

class A98RGB(sRGB):
    BASE: str
    NAME: str
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
