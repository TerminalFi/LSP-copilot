from ..cat import WHITES as WHITES
from ..channels import Channel as Channel
from ..spaces import Space as Space
from ..types import Vector as Vector
from _typeshed import Incomplete

def srgb_to_cmyk(rgb: Vector) -> Vector: ...
def cmyk_to_srgb(cmyk: Vector) -> Vector: ...

class CMYK(Space):
    BASE: str
    NAME: str
    SERIALIZE: tuple[str, ...]
    CHANNELS: Incomplete
    CHANNEL_ALIASES: Incomplete
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
