from ... import util as util
from ...cat import WHITES as WHITES
from ...channels import Channel as Channel, FLG_ANGLE as FLG_ANGLE, FLG_OPT_PERCENT as FLG_OPT_PERCENT
from ...spaces import LChish as LChish, Space as Space
from ...types import Vector as Vector
from _typeshed import Incomplete

ACHROMATIC_THRESHOLD: float

def lab_to_lch(lab: Vector) -> Vector: ...
def lch_to_lab(lch: Vector) -> Vector: ...

class LCh(LChish, Space):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    WHITE: Incomplete
    def normalize(self, coords: Vector) -> Vector: ...
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
