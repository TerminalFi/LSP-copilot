from .fit_lch_chroma import LChChroma as LChChroma

class OkLChChroma(LChChroma):
    NAME: str
    EPSILON: float
    LIMIT: float
    DE: str
    SPACE: str
    MAX_LIGHTNESS: int
