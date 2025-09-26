# This file is maintained on https://github.com/jfcherng-sublime/ST-API-stubs

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Protocol, Sequence, Tuple, TypedDict, TypeVar

import sublime

# ----- #
# types #
# ----- #

T = TypeVar("T")

AnyCallable = Callable[..., Any]
Callback0 = Callable[[], Any]
Callback1 = Callable[[T], Any]

T_AnyCallable = TypeVar("T_AnyCallable", bound=AnyCallable)
T_ExpandableVar = TypeVar(
    "T_ExpandableVar",
    bound=None | bool | int | float | str | Dict[Any, Any] | List[Any] | Tuple[Any, ...],
)

Point = int
Dip = float
Str = str  # alias in case we have a variable named as "str"

Completion = str | Sequence[str] | Tuple[str, str] | sublime.CompletionItem
CompletionKind = Tuple[int, str, str]
CompletionNormalized = Tuple[
    str,  # trigger
    str,  # annotation
    str,  # details
    str,  # completion
    str,  # kind_name
    int,  # icon letter (Unicode code point, decimal form)
    int,  # completion_format
    int,  # flags
    int,  # kind
]

Location = Tuple[str, str, Tuple[int, int]]
Vector = Tuple[Dip, Dip]


class Layout(TypedDict):
    cols: List[float]
    rows: List[float]
    cells: List[List[int]]


class EventDict(TypedDict):
    x: float
    y: float
    modifier_keys: EventModifierKeysDict


class EventModifierKeysDict(TypedDict, total=False):
    primary: bool
    ctrl: bool
    alt: bool
    altgr: bool
    shift: bool
    super: bool


class ExtractVariablesDict(TypedDict):
    file: str
    file_base_name: str
    file_extension: str
    file_name: str
    file_path: str
    folder: str
    packages: str
    platform: str
    project: str
    project_base_name: str
    project_extension: str
    project_name: str
    project_path: str


class ScopeStyleDict(TypedDict, total=False):
    foreground: str
    background: str
    bold: bool
    italic: bool
    glow: bool
    underline: bool
    stippled_underline: bool
    squiggly_underline: bool
    source_line: int
    source_column: int
    source_file: str


class CommandArgsDict(TypedDict):
    command: str
    args: None | Dict[str, Any]


class HasKeysMethod(Protocol):
    def keys(self) -> Iterable[str]:
        ...
