from ..channels import Channel as Channel
from ..spaces.srgb import sRGB as sRGB
from ..types import Vector as Vector
from .acescc import CC_MAX as CC_MAX
from _typeshed import Incomplete

CCT_MIN: float
CCT_MAX = CC_MAX
C1: float
C2: float
C3: float

def acescct_to_acescg(acescc: Vector) -> Vector: ...
def acescg_to_acescct(acescg: Vector) -> Vector: ...

class ACEScct(sRGB):
    BASE: str
    NAME: str
    SERIALIZE: tuple[str, ...]
    WHITE: Incomplete
    CHANNELS: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
