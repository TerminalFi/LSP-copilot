from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_MIRROR_PERCENT as FLG_MIRROR_PERCENT
from ..types import Vector as Vector
from .lab import Lab as Lab
from _typeshed import Incomplete

KE: int
KCH: int
RADS: Incomplete
FACTOR: float
C1: Incomplete
C2: float
C3: float
C4: float

def lab_to_din99o(lab: Vector) -> Vector: ...
def din99o_lab_to_lch(lab: Vector) -> Vector: ...
def din99o_to_lab(din99o: Vector) -> Vector: ...

class DIN99o(Lab):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    WHITE: Incomplete
    CHANNELS: Incomplete
    def to_base(self, coords: Vector) -> Vector: ...
    def from_base(self, coords: Vector) -> Vector: ...
