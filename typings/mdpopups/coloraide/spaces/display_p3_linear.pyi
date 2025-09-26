from ..cat import WHITES as WHITES
from ..types import Vector as Vector
from .srgb import sRGB as sRGB
from _typeshed import Incomplete

RGB_TO_XYZ: Incomplete
XYZ_TO_RGB: Incomplete

def lin_p3_to_xyz(rgb: Vector) -> Vector: ...
def xyz_to_lin_p3(xyz: Vector) -> Vector: ...

class DisplayP3Linear(sRGB):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
