from ...cat import WHITES as WHITES
from ...channels import Channel as Channel, FLG_MIRROR_PERCENT as FLG_MIRROR_PERCENT, FLG_OPT_PERCENT as FLG_OPT_PERCENT
from ...spaces import Labish as Labish, Space as Space
from ...types import Vector as Vector
from _typeshed import Incomplete

SRGBL_TO_LMS: Incomplete
LMS_TO_SRGBL: Incomplete
LMS3_TO_OKLAB: Incomplete
OKLAB_TO_LMS3: Incomplete
XYZD65_TO_LMS: Incomplete
LMS_TO_XYZD65: Incomplete

def oklab_to_linear_srgb(lab: Vector) -> Vector: ...
def linear_srgb_to_oklab(rgb: Vector) -> Vector: ...
def oklab_to_xyz_d65(lab: Vector) -> Vector: ...
def xyz_d65_to_oklab(xyz: Vector) -> Vector: ...

class Oklab(Labish, Space):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    WHITE: Incomplete
    def to_base(self, oklab: Vector) -> Vector: ...
    def from_base(self, xyz: Vector) -> Vector: ...
