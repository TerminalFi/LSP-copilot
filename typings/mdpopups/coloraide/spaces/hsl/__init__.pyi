from ... import util as util
from ...cat import WHITES as WHITES
from ...channels import Channel as Channel, FLG_ANGLE as FLG_ANGLE, FLG_PERCENT as FLG_PERCENT
from ...spaces import Cylindrical as Cylindrical, Space as Space
from ...types import Vector as Vector
from _typeshed import Incomplete

def srgb_to_hsl(rgb: Vector) -> Vector: ...
def hsl_to_srgb(hsl: Vector) -> Vector: ...

class HSL(Cylindrical, Space):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    WHITE: Incomplete
    GAMUT_CHECK: str
    def normalize(self, coords: Vector) -> Vector: ...
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
