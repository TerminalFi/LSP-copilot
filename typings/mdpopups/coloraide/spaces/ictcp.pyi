from .. import util as util
from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_MIRROR_PERCENT as FLG_MIRROR_PERCENT
from ..spaces import Labish as Labish, Space as Space
from ..types import Vector as Vector
from _typeshed import Incomplete

xyz_to_lms_m: Incomplete
lms_to_xyz_mi: Incomplete
lms_p_to_ictcp_m: Incomplete
ictcp_to_lms_p_mi: Incomplete

def ictcp_to_xyz_d65(ictcp: Vector) -> Vector: ...
def xyz_d65_to_ictcp(xyzd65: Vector) -> Vector: ...

class ICtCp(Labish, Space):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    CHANNELS: Incomplete
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
