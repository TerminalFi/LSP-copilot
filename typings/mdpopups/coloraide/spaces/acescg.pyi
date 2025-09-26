from ..channels import Channel as Channel
from ..spaces.srgb import sRGB as sRGB
from ..types import Vector as Vector
from _typeshed import Incomplete

AP1_TO_XYZ: Incomplete
XYZ_TO_AP1: Incomplete

def acescg_to_xyz(acescg: Vector) -> Vector: ...
def xyz_to_acescg(xyz: Vector) -> Vector: ...

class ACEScg(sRGB):
    BASE: str
    NAME: str
    SERIALIZE: tuple[str, ...]
    WHITE: Incomplete
    CHANNELS: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
