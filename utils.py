import os
import textwrap

import sublime
from LSP.plugin.core.sessions import Session
from LSP.plugin.core.typing import Any, List, Optional, TypeVar, Union

from .constants import COPILOT_VIEW_SETTINGS_PREFIX
from .types import CopilotPayloadCompletion

T_Number = TypeVar("T_Number", bound=Union[int, float])


def clamp(val: T_Number, min_val: Optional[T_Number] = None, max_val: Optional[T_Number] = None) -> T_Number:
    """Returns the bounded value of `val` in the range of `[min_val, max_val]`."""
    if min_val is not None and val < min_val:  # type: ignore
        return min_val
    if max_val is not None and val > max_val:  # type: ignore
        return max_val
    return val


def get_copilot_view_setting(view: sublime.View, key: str, default: Any = None) -> Any:
    return view.settings().get("{}.{}".format(COPILOT_VIEW_SETTINGS_PREFIX, key), default)


def set_copilot_view_setting(view: sublime.View, key: str, value: Any) -> None:
    view.settings().set("{}.{}".format(COPILOT_VIEW_SETTINGS_PREFIX, key), value)


def erase_copilot_view_setting(view: sublime.View, key: str) -> None:
    view.settings().erase("{}.{}".format(COPILOT_VIEW_SETTINGS_PREFIX, key))


def get_project_relative_path(file_path: str) -> str:
    ret = file_path
    for folder in sublime.active_window().folders():
        try:
            ret = min(ret, os.path.relpath(file_path, folder), key=len)
        except ValueError:
            pass
    return ret


def get_setting(session: Session, key: str, default: Optional[Union[str, bool, List[str]]] = None) -> Any:
    value = session.config.settings.get(key)
    if value is None:
        return default
    return value


def preprocess_completions(view: sublime.View, completions: List[CopilotPayloadCompletion]) -> None:
    for completion in completions:
        completion["positionSt"] = view.text_point(
            completion["position"]["line"],
            completion["position"]["character"],
        )


def reformat(text: str) -> str:
    """Remove common indentations and then trim."""
    return textwrap.dedent(text).strip()
