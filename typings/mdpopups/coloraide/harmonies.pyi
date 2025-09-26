from .color import Color as Color
from .spaces import Cylindrical as Cylindrical

class Harmony:
    def harmonize(self, color: Color, space: str | None) -> list['Color']: ...

class Monochromatic(Harmony):
    DELTA_E: str
    RANGE: int
    STEPS: int
    def harmonize(self, color: Color, space: str | None) -> list['Color']: ...

class Geometric(Harmony):
    COUNT: int
    def harmonize(self, color: Color, space: str | None) -> list['Color']: ...

class Complementary(Geometric):
    COUNT: int

class Triadic(Geometric):
    COUNT: int

class TetradicSquare(Geometric):
    COUNT: int

class SplitComplementary(Harmony):
    def harmonize(self, color: Color, space: str | None) -> list['Color']: ...

class Analogous(Harmony):
    def harmonize(self, color: Color, space: str | None) -> list['Color']: ...

class TetradicRect(Harmony):
    def harmonize(self, color: Color, space: str | None) -> list['Color']: ...

SUPPORTED: dict[str, Harmony]

def harmonize(color: Color, name: str, space: str | None) -> list['Color']: ...
