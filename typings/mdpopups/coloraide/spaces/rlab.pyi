from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_MIRROR_PERCENT as FLG_MIRROR_PERCENT
from ..spaces.lab import Lab as Lab
from ..types import Vector as Vector
from _typeshed import Incomplete

XYZ_TO_XYZ_REF: Incomplete
XYZ_REF_TO_XYZ: Incomplete
EXP: float

def rlab_to_xyz(rlab: Vector) -> Vector: ...
def xyz_to_rlab(xyz: Vector) -> Vector: ...

class RLAB(Lab):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    WHITE: Incomplete
    CHANNELS: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
