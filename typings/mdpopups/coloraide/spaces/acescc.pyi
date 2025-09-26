from ..channels import Channel as Channel
from ..spaces.srgb import sRGB as sRGB
from ..types import Vector as Vector
from _typeshed import Incomplete

CC_MIN: Incomplete
CC_MAX: Incomplete

def acescc_to_acescg(acescc: Vector) -> Vector: ...
def acescg_to_acescc(acescg: Vector) -> Vector: ...

class ACEScc(sRGB):
    BASE: str
    NAME: str
    SERIALIZE: tuple[str, ...]
    WHITE: Incomplete
    CHANNELS: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
