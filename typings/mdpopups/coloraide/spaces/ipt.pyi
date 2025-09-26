from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_MIRROR_PERCENT as FLG_MIRROR_PERCENT
from ..spaces import Labish as Labish, Space as Space
from ..types import Vector as Vector
from _typeshed import Incomplete

XYZ_TO_LMS: Incomplete
LMS_TO_XYZ: Incomplete
LMS_P_TO_IPT: Incomplete
IPT_TO_LMS_P: Incomplete

def xyz_to_ipt(xyz: Vector) -> Vector: ...
def ipt_to_xyz(ipt: Vector) -> Vector: ...

class IPT(Labish, Space):
    BASE: str
    NAME: str
    SERIALIZE: tuple[str, ...]
    CHANNELS: Incomplete
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
