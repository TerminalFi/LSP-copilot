from .. import util as util
from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_ANGLE as FLG_ANGLE
from ..spaces import Cylindrical as Cylindrical, Space as Space
from ..types import Vector as Vector
from .okhsl import find_cusp as find_cusp, to_st as to_st, toe as toe, toe_inv as toe_inv
from .oklab import oklab_to_linear_srgb as oklab_to_linear_srgb
from .oklch import ACHROMATIC_THRESHOLD as ACHROMATIC_THRESHOLD
from _typeshed import Incomplete

def okhsv_to_oklab(hsv: Vector) -> Vector: ...
def oklab_to_okhsv(lab: Vector) -> Vector: ...

class Okhsv(Cylindrical, Space):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    WHITE: Incomplete
    GAMUT_CHECK: str
    def normalize(self, coords: Vector) -> Vector: ...
    def to_base(self, okhsv: Vector) -> Vector: ...
    def from_base(self, oklab: Vector) -> Vector: ...
