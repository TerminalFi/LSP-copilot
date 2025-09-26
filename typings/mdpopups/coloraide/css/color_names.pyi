from ..types import Vector as Vector

name2val_map: dict[str, tuple[float, ...]]
val2name_map: dict[tuple[float, ...], str]

def to_name(value: Vector) -> str | None: ...
def from_name(name: str) -> Vector | None: ...
