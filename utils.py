import os
import textwrap

import sublime
from LSP.plugin.core.sessions import Session
from LSP.plugin.core.types import basescope2languageid
from LSP.plugin.core.typing import Any, Callable, Dict, Generator, Iterable, List, Optional, TypeVar, Union
from LSP.plugin.core.url import filename_to_uri

from .constants import COPILOT_VIEW_SETTINGS_PREFIX
from .types import CopilotPayloadCompletion

T = TypeVar("T")
T_Number = TypeVar("T_Number", bound=Union[int, float])


def all_st_views(*, include_transient: bool = False) -> Generator[sublime.View, None, None]:
    for window in sublime.windows():
        yield from window.views(include_transient=include_transient)


def clamp(val: T_Number, min_val: Optional[T_Number] = None, max_val: Optional[T_Number] = None) -> T_Number:
    """Returns the bounded value of `val` in the range of `[min_val, max_val]`."""
    if min_val is not None and val < min_val:  # type: ignore
        return min_val
    if max_val is not None and val > max_val:  # type: ignore
        return max_val
    return val


def first(items: Iterable[T], test: Optional[Callable[[T], bool]] = None, default: Optional[T] = None) -> Optional[T]:
    """
    Gets the first item which satisfies the `test`. Otherwise, `default`.
    If `test` is not given or `None`, the first truthy item will be returned.
    """
    return next(filter(test, items), default)


def get_copilot_view_setting(view: sublime.View, key: str, default: Any = None) -> Any:
    return view.settings().get("{}.{}".format(COPILOT_VIEW_SETTINGS_PREFIX, key), default)


def set_copilot_view_setting(view: sublime.View, key: str, value: Any) -> None:
    view.settings().set("{}.{}".format(COPILOT_VIEW_SETTINGS_PREFIX, key), value)


def erase_copilot_view_setting(view: sublime.View, key: str) -> None:
    view.settings().erase("{}.{}".format(COPILOT_VIEW_SETTINGS_PREFIX, key))


def get_project_relative_path(path: str) -> str:
    relpath = path
    for folder in sublime.active_window().folders():
        try:
            relpath = min(relpath, os.path.relpath(path, folder), key=len)
        except ValueError:
            pass
    return relpath


def get_setting(session: Session, key: str, default: Optional[Union[str, bool, List[str]]] = None) -> Any:
    value = session.config.settings.get(key)
    if value is None:
        return default
    return value


def prepare_completion_request(view: sublime.View) -> Optional[Dict[str, Any]]:
    syntax = view.syntax()
    sel = view.sel()
    if not (syntax and len(sel) == 1):
        return None

    file_path = view.file_name() or ""
    row, col = view.rowcol(sel[0].begin())
    return {
        "doc": {
            "source": view.substr(sublime.Region(0, view.size())),
            "tabSize": view.settings().get("tab_size", 4),
            "indentSize": 1,  # there is no such concept in ST
            "insertSpaces": view.settings().get("translate_tabs_to_spaces", False),
            "path": file_path,
            "uri": file_path and filename_to_uri(file_path),
            "relativePath": get_project_relative_path(file_path),
            "languageId": basescope2languageid(syntax.scope),
            "position": {"line": row, "character": col},
        }
    }


def preprocess_completions(view: sublime.View, completions: List[CopilotPayloadCompletion]) -> None:
    for completion in completions:
        completion["positionSt"] = view.text_point(
            completion["position"]["line"],
            completion["position"]["character"],
        )


def reformat(text: str) -> str:
    """Remove common indentations and then trim."""
    return textwrap.dedent(text).strip()


def remove_prefix(s: str, prefix: str) -> str:
    """Remove the prefix from the string. I.e., str.removeprefix in Python 3.9."""
    return s[len(prefix) :] if s.startswith(prefix) else s


def remove_suffix(s: str, suffix: str) -> str:
    """Remove the suffix from the string. I.e., str.removesuffix in Python 3.9."""
    # suffix="" should not call s[:-0]
    return s[: -len(suffix)] if suffix and s.endswith(suffix) else s


def unique(items: Iterable[T], key: Optional[Callable[[T], Any]] = None) -> Generator[T, None, None]:
    key = key or (lambda x: x)
    seen = set()
    for item in items:
        k = key(item)
        if k in seen:
            continue

        yield item
        seen.add(k)
