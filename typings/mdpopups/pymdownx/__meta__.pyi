from _typeshed import Incomplete
from typing import NamedTuple

RE_VER: Incomplete
REL_MAP: Incomplete
DEV_STATUS: Incomplete
PRE_REL_MAP: Incomplete

class Version(NamedTuple('Version', [('major', Incomplete), ('minor', Incomplete), ('micro', Incomplete), ('release', Incomplete), ('pre', Incomplete), ('post', Incomplete), ('dev', Incomplete)])):
    def __new__(cls, major, minor, micro, release: str = 'final', pre: int = 0, post: int = 0, dev: int = 0): ...

def parse_version(ver, pre: bool = False): ...

__version_info__: Incomplete
__version__: Incomplete
