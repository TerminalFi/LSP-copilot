from .. import util as util
from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_ANGLE as FLG_ANGLE
from ..spaces import Cylindrical as Cylindrical, Space as Space
from ..types import Vector as Vector
from .lab import EPSILON as EPSILON, KAPPA as KAPPA
from .lch import ACHROMATIC_THRESHOLD as ACHROMATIC_THRESHOLD
from .srgb_linear import XYZ_TO_RGB as XYZ_TO_RGB
from _typeshed import Incomplete

def length_of_ray_until_intersect(theta: float, line: dict[str, float]) -> float: ...
def get_bounds(l: float) -> list[dict[str, float]]: ...
def max_chroma_for_lh(l: float, h: float) -> float: ...
def hsluv_to_lch(hsluv: Vector) -> Vector: ...
def lch_to_hsluv(lch: Vector) -> Vector: ...

class HSLuv(Cylindrical, Space):
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
