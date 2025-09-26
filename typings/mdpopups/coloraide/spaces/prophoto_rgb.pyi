from ..cat import WHITES as WHITES
from ..types import Vector as Vector
from .srgb import sRGB as sRGB
from _typeshed import Incomplete

ET: Incomplete
ET2: Incomplete

def lin_prophoto(rgb: Vector) -> Vector: ...
def gam_prophoto(rgb: Vector) -> Vector: ...

class ProPhotoRGB(sRGB):
    BASE: str
    NAME: str
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
