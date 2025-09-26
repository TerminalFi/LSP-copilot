from .. import util as util
from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_MIRROR_PERCENT as FLG_MIRROR_PERCENT
from ..spaces import Labish as Labish, Space as Space
from ..types import Vector as Vector
from _typeshed import Incomplete

B: float
G: float
D: float
D0: float
M2: Incomplete
xyz_to_lms_m: Incomplete
lms_to_xyz_mi: Incomplete
lms_p_to_izazbz_m: Incomplete
izazbz_to_lms_p_mi: Incomplete

def jzazbz_to_xyz_d65(jzazbz: Vector) -> Vector: ...
def xyz_d65_to_jzazbz(xyzd65: Vector) -> Vector: ...

class Jzazbz(Labish, Space):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
