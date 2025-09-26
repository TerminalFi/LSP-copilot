from .. import util as util
from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_ANGLE as FLG_ANGLE
from ..types import Vector as Vector
from .lch import LCh as LCh
from _typeshed import Incomplete

ACHROMATIC_THRESHOLD: float

def lch_to_lab(lch: Vector) -> Vector: ...
def lab_to_lch(lab: Vector) -> Vector: ...

class LCh99o(LCh):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    WHITE: Incomplete
    CHANNELS: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
