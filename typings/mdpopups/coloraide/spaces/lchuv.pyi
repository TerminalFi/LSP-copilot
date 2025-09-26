from .. import util as util
from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_ANGLE as FLG_ANGLE
from ..spaces import Space as Space
from ..types import Vector as Vector
from .lch import ACHROMATIC_THRESHOLD as ACHROMATIC_THRESHOLD, LCh as LCh
from _typeshed import Incomplete

def luv_to_lchuv(luv: Vector) -> Vector: ...
def lchuv_to_luv(lchuv: Vector) -> Vector: ...

class LChuv(LCh, Space):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    WHITE: Incomplete
    CHANNELS: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
