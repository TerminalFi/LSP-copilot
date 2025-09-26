from ... import util as util
from ...cat import WHITES as WHITES
from ...channels import Channel as Channel, FLG_MIRROR_PERCENT as FLG_MIRROR_PERCENT, FLG_OPT_PERCENT as FLG_OPT_PERCENT
from ...spaces import Labish as Labish, Space as Space
from ...types import Vector as Vector, VectorLike as VectorLike
from _typeshed import Incomplete

EPSILON: Incomplete
EPSILON3: Incomplete
KAPPA: Incomplete
KE: int

def lab_to_xyz(lab: Vector, white: VectorLike) -> Vector: ...
def xyz_to_lab(xyz: Vector, white: VectorLike) -> Vector: ...

class Lab(Labish, Space):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
