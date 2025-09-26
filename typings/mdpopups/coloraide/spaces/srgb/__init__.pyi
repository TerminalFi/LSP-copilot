from ...cat import WHITES as WHITES
from ...channels import Channel as Channel, FLG_OPT_PERCENT as FLG_OPT_PERCENT
from ...spaces import Space as Space
from ...types import Vector as Vector
from _typeshed import Incomplete

def lin_srgb(rgb: Vector) -> Vector: ...
def gam_srgb(rgb: Vector) -> Vector: ...

class sRGB(Space):
    BASE: str
    NAME: str
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    WHITE: Incomplete
    EXTENDED_RANGE: bool
    def from_base(self, coords: Vector) -> Vector: ...
    def to_base(self, coords: Vector) -> Vector: ...
