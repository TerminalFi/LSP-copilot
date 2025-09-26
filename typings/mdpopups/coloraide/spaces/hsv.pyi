from .. import util as util
from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_ANGLE as FLG_ANGLE
from ..spaces import Cylindrical as Cylindrical, Space as Space
from ..types import Vector as Vector
from _typeshed import Incomplete

def hsv_to_hsl(hsv: Vector) -> Vector: ...
def hsl_to_hsv(hsl: Vector) -> Vector: ...

class HSV(Cylindrical, Space):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    GAMUT_CHECK: str
    WHITE: Incomplete
    def normalize(self, coords: Vector) -> Vector: ...
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
