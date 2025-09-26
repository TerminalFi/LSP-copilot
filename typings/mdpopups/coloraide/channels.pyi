FLG_ANGLE: int
FLG_PERCENT: int
FLG_OPT_PERCENT: int
FLG_MIRROR_PERCENT: int

class Channel(str):
    def __new__(cls, name: str, low: float, high: float, mirror_range: bool = False, bound: bool = False, flags: int = 0, limit: tuple[float | None, float | None] = (None, None)) -> Channel: ...
