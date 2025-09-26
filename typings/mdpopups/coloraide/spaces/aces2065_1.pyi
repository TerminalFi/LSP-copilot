from ..channels import Channel as Channel
from ..spaces.srgb import sRGB as sRGB
from ..types import Vector as Vector
from _typeshed import Incomplete

AP0_TO_XYZ: Incomplete
XYZ_TO_AP0: Incomplete
MIN: float
MAX: float

def aces_to_xyz(aces: Vector) -> Vector: ...
def xyz_to_aces(xyz: Vector) -> Vector: ...

class ACES20651(sRGB):
    BASE: str
    NAME: str
    SERIALIZE: tuple[str, ...]
    WHITE: Incomplete
    CHANNELS: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
