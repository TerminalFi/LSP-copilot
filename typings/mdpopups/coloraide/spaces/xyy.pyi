from .. import util as util
from ..cat import WHITES as WHITES
from ..channels import Channel as Channel
from ..spaces import Space as Space
from ..types import Vector as Vector
from _typeshed import Incomplete

class xyY(Space):
    BASE: str
    NAME: str
    SERIALIZE: tuple[str, ...]
    CHANNELS: Incomplete
    WHITE: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
