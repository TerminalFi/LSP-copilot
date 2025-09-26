from ..cat import WHITES as WHITES
from ..channels import Channel as Channel, FLG_MIRROR_PERCENT as FLG_MIRROR_PERCENT
from .lab import Lab as Lab
from _typeshed import Incomplete

class LabD65(Lab):
    BASE: str
    NAME: str
    SERIALIZE: Incomplete
    WHITE: Incomplete
    CHANNELS: Incomplete
