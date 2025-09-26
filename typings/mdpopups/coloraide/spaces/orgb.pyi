from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_MIRROR_PERCENT as FLG_MIRROR_PERCENT
from ..spaces import Labish as Labish, Space as Space
from ..types import Vector as Vector
from _typeshed import Incomplete

RGB_TO_LC1C2: Incomplete
LC1C2_TO_RGB: Incomplete

def rotate(v: Vector, d: float) -> Vector: ...
def srgb_to_orgb(rgb: Vector) -> Vector: ...
def orgb_to_srgb(lcc: Vector) -> Vector: ...

class oRGB(Labish, Space):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    WHITE: Incomplete
    EXTENDED_RANGE: bool
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
