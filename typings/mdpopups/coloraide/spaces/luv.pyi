from .. import util as util
from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_MIRROR_PERCENT as FLG_MIRROR_PERCENT
from ..spaces import Labish as Labish, Space as Space
from ..types import Vector as Vector
from .lab import EPSILON as EPSILON, KAPPA as KAPPA, KE as KE
from _typeshed import Incomplete

def xyz_to_luv(xyz: Vector, white: tuple[float, float]) -> Vector: ...
def luv_to_xyz(luv: Vector, white: tuple[float, float]) -> Vector: ...

class Luv(Labish, Space):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
