from ..cat import WHITES as WHITES
from ..channels import Channel as Channel
from ..spaces import Space as Space
from ..types import Vector as Vector
from _typeshed import Incomplete

def srgb_to_lrgb(rgb: Vector) -> Vector: ...
def lrgb_to_srgb(lrgb: Vector) -> Vector: ...

class Prismatic(Space):
    BASE: str
    NAME: str
    SERIALIZE: tuple[str, ...]
    EXTENDED_RANGE: bool
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
