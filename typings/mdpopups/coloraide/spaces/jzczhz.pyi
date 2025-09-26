from .. import util as util
from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_ANGLE as FLG_ANGLE
from ..spaces import LChish as LChish, Space as Space
from ..types import Vector as Vector
from _typeshed import Incomplete

ACHROMATIC_THRESHOLD: float

def jzazbz_to_jzczhz(jzazbz: Vector) -> Vector: ...
def jzczhz_to_jzazbz(jzczhz: Vector) -> Vector: ...

class JzCzhz(LChish, Space):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    WHITE: Incomplete
    def normalize(self, coords: Vector) -> Vector: ...
    def hue_name(self) -> str: ...
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
