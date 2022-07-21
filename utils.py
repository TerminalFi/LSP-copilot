import os
import textwrap

import sublime
from LSP.plugin.core.sessions import Session
from LSP.plugin.core.types import basescope2languageid
from LSP.plugin.core.typing import Any, Callable, Dict, Generator, Iterable, List, Optional, TypeVar, Union
from LSP.plugin.core.url import filename_to_uri

from .constants import COPILOT_VIEW_SETTINGS_PREFIX, PACKAGE_NAME
from .types import CopilotPayloadCompletion, CopilotPayloadPanelSolution

T = TypeVar("T")
T_Number = TypeVar("T_Number", bound=Union[int, float])


def all_views(*, include_transient: bool = False) -> Generator[sublime.View, None, None]:
    for window in sublime.windows():
        yield from window.views(include_transient=include_transient)


def all_sheets() -> Generator[sublime.Sheet, None, None]:
    for window in sublime.windows():
        yield from window.sheets()


def clamp(val: T_Number, min_val: Optional[T_Number] = None, max_val: Optional[T_Number] = None) -> T_Number:
    """Returns the bounded value of `val` in the range of `[min_val, max_val]`."""
    if min_val is not None and val < min_val:  # type: ignore
        return min_val
    if max_val is not None and val > max_val:  # type: ignore
        return max_val
    return val


def find_sheet_by_id(id: int) -> Optional[sublime.Sheet]:
    return first(all_sheets(), lambda sheet: sheet.id() == id)


def find_view_by_id(id: int, *, include_transient: bool = False) -> Optional[sublime.View]:
    return first(all_views(include_transient=include_transient), lambda view: view.id() == id)


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


def get_view_syntax(view: sublime.View) -> sublime.Syntax:
    return view.syntax() or sublime.find_syntax_by_name("Plain Text")[0]


def message_dialog(msg: str, *, console: bool = False) -> None:
    full_msg = "[{}] {}".format(PACKAGE_NAME, msg)
    sublime.message_dialog(full_msg)

    if console:
        print(full_msg)


def ok_cancel_dialog(msg: str) -> bool:
    return sublime.ok_cancel_dialog("[{}] {}".format(PACKAGE_NAME, msg))


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
        completion["point"] = view.text_point(
            completion["position"]["line"],
            completion["position"]["character"],
        )
        _generate_completion_region(view, completion)


def preprocess_panel_completions(view: sublime.View, completions: List[CopilotPayloadPanelSolution]) -> None:
    for completion in completions:
        _generate_completion_region(view, completion)


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


def status_message(msg: str, *, icon: Optional[str] = "✈", console: bool = False) -> None:
    prefix = "{} ".format(icon) if icon else ""
    full_msg = "{}Copilot {}".format(prefix, msg)
    sublime.status_message(full_msg)

    if console:
        print(full_msg)


def unique(items: Iterable[T], key: Optional[Callable[[T], Any]] = None) -> Generator[T, None, None]:
    key = key or (lambda x: x)
    seen = set()
    for item in items:
        k = key(item)
        if k not in seen:
            yield item
            seen.add(k)


def _generate_completion_region(
    view: sublime.View,
    completion: Union[CopilotPayloadCompletion, CopilotPayloadPanelSolution],
) -> None:
    completion["region"] = (
        view.text_point(
            completion["range"]["start"]["line"],
            completion["range"]["start"]["character"],
        ),
        view.text_point(
            completion["range"]["end"]["line"],
            completion["range"]["end"]["character"],
        ),
    )
