from .. import util as util
from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_MIRROR_PERCENT as FLG_MIRROR_PERCENT
from ..spaces.lab import Lab as Lab
from ..types import Vector as Vector, VectorLike as VectorLike
from _typeshed import Incomplete

CXN: float
CYN: float
CZN: float
CKA: float
CKB: float

def xyz_to_hlab(xyz: Vector, white: VectorLike) -> Vector: ...
def hlab_to_xyz(hlab: Vector, white: VectorLike) -> Vector: ...

class HunterLab(Lab):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    WHITE: Incomplete
    CHANNELS: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
