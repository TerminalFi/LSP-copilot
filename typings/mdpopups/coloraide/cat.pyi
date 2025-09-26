from . import util as util
from .types import Matrix as Matrix, Plugin as Plugin, Vector as Vector, VectorLike as VectorLike
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from typing import Any

WHITES: Incomplete

def calc_adaptation_matrices(w1: tuple[float, float], w2: tuple[float, float], m: Matrix) -> tuple[Matrix, Matrix]: ...

class VonKriesMeta(ABCMeta):
    def __init__(cls, name: str, bases: tuple[object, ...], clsdict: dict[str, Any]) -> None: ...

class CAT(Plugin, metaclass=ABCMeta):
    NAME: str
    @abstractmethod
    def adapt(self, w1: tuple[float, float], w2: tuple[float, float], xyz: VectorLike) -> Vector: ...

class VonKries(CAT, metaclass=VonKriesMeta):
    NAME: str
    MATRIX: Matrix
    def adapt(self, w1: tuple[float, float], w2: tuple[float, float], xyz: VectorLike) -> Vector: ...

class Bradford(VonKries):
    NAME: str
    MATRIX: Incomplete

class XYZScaling(VonKries):
    NAME: str
    MATRIX: Incomplete

class CAT02(VonKries):
    NAME: str
    MATRIX: Incomplete

class CMCCAT97(VonKries):
    NAME: str
    MATRIX: Incomplete

class Sharp(VonKries):
    NAME: str
    MATRIX: Incomplete

class CMCCAT2000(VonKries):
    NAME: str
    MATRIX: Incomplete

class CAT16(VonKries):
    NAME: str
    MATRIX: Incomplete
