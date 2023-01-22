import os
import textwrap
import threading
import traceback
from functools import wraps
from itertools import takewhile
from operator import itemgetter

import sublime
from LSP.plugin.core.sessions import Session
from LSP.plugin.core.types import basescope2languageid
from LSP.plugin.core.typing import Any, Callable, Dict, Generator, Iterable, List, Optional, Set, TypeVar, Union, cast
from LSP.plugin.core.url import filename_to_uri

from .constants import COPILOT_VIEW_SETTINGS_PREFIX, PACKAGE_NAME
from .types import CopilotPayloadCompletion, CopilotPayloadPanelSolution, T_Callable

T = TypeVar("T")
T_Number = TypeVar("T_Number", bound=Union[int, float])


def all_views(
    window: Optional[sublime.Window] = None,
    *,
    include_transient: bool = False
    # format delimiter
) -> Generator[sublime.View, None, None]:
    windows = [window] if window else sublime.windows()
    for window in windows:
        yield from window.views(include_transient=include_transient)


def all_sheets(
    window: Optional[sublime.Window] = None,
    *,
    include_transient: bool = False
    # format delimiter
) -> Generator[sublime.Sheet, None, None]:
    windows = [window] if window else sublime.windows()
    for window in windows:
        if include_transient:
            yield from filter(None, map(window.transient_sheet_in_group, range(window.num_groups())))
        yield from window.sheets()


def clamp(val: T_Number, min_val: Optional[T_Number] = None, max_val: Optional[T_Number] = None) -> T_Number:
    """Returns the bounded value of `val` in the range of `[min_val, max_val]`."""
    if min_val is not None and val < min_val:  # type: ignore
        return min_val
    if max_val is not None and val > max_val:  # type: ignore
        return max_val
    return val


def debounce(time_s: float = 0.3) -> Callable[[T_Callable], T_Callable]:
    """
    Debounce a function so that it's called after `time_s` seconds.
    If it's called multiple times in the time frame, it will only run the last call.

    Taken and modified from https://github.com/salesforce/decorator-operations
    """

    def decorator(func: T_Callable) -> T_Callable:
        @wraps(func)
        def debounced(*args: Any, **kwargs: Any) -> None:
            def call_function() -> Any:
                delattr(debounced, "_timer")
                return func(*args, **kwargs)

            timer = getattr(debounced, "_timer", None)  # type: Optional[threading.Timer]
            if timer is not None:
                timer.cancel()

            timer = threading.Timer(time_s, call_function)
            timer.start()
            setattr(debounced, "_timer", timer)

        setattr(debounced, "_timer", None)
        return cast(T_Callable, debounced)

    return decorator


def find_sheet_by_id(id: int) -> Optional[sublime.Sheet]:
    return first(all_sheets(include_transient=True), lambda sheet: sheet.id() == id)


def find_view_by_id(id: int) -> Optional[sublime.View]:
    return first(all_views(include_transient=True), lambda view: view.id() == id)


def first(items: Iterable[T], test: Optional[Callable[[T], bool]] = None, default: Optional[T] = None) -> Optional[T]:
    """
    Gets the first item which satisfies the `test`. Otherwise, `default`.
    If `test` is not given or `None`, the first truthy item will be returned.
    """
    return next(filter(test, items), default)


def fix_completion_syntax_highlight(view: sublime.View, point: int, code: str) -> str:
    if view.match_selector(point, "source.php"):
        return "<?php\n{}".format(code)
    return code


def get_copilot_view_setting(view: sublime.View, key: str, default: Any = None) -> Any:
    return view.settings().get("{}.{}".format(COPILOT_VIEW_SETTINGS_PREFIX, key), default)


def set_copilot_view_setting(view: sublime.View, key: str, value: Any) -> None:
    view.settings().set("{}.{}".format(COPILOT_VIEW_SETTINGS_PREFIX, key), value)


def erase_copilot_view_setting(view: sublime.View, key: str) -> None:
    view.settings().erase("{}.{}".format(COPILOT_VIEW_SETTINGS_PREFIX, key))


def get_project_relative_path(path: str) -> str:
    """Get the relative path regarding the project root directory. If not possible, return the path as-is."""
    relpath = path
    for folder in sublime.active_window().folders():
        try:
            relpath = min(relpath, os.path.relpath(path, folder), key=len)
        except ValueError:
            pass
    return relpath


def get_session_setting(session: Session, key: str, default: Any = None) -> Any:
    """Get the value of the `key` in "settings" in this plugin's "LSP-*.sublime-settings"."""
    value = session.config.settings.get(key)
    return default if value is None else value


def get_view_language_id(view: sublime.View, point: int = 0) -> str:
    """Find the language ID for the `view` at `point`."""
    # the deepest scope satisfying `source | text | embedding` will be used to find language ID
    for scope in reversed(view.scope_name(point).split(" ")):
        if sublime.score_selector(scope, "source | text | embedding"):
            # For some embedded languages, they are scoped as "EMBEDDED_LANG.embedded.PARENT_LANG"
            # such as "source.php.embedded.html" and we only want those parts before "embedded".
            return basescope2languageid(".".join(takewhile(lambda s: s != "embedded", scope.split("."))))
    return ""


def message_dialog(msg_: str, *args, error_: bool = False, console_: bool = False, **kwargs) -> None:
    """
    Show a message dialog, whose message is prefixed with "[PACKAGE_NAME]".

    :param      msg_:      The message
    :param      args:      The arguments for `str.format`
    :param      error_:    The error
    :param      console_:  Show message in console as well?
    :param      kwargs:    The keywords arguments for `str.format`
    """
    full_msg = "[{}] {}".format(PACKAGE_NAME, msg_.format(*args, **kwargs))
    messenger = sublime.error_message if error_ else sublime.message_dialog
    messenger(full_msg)

    if console_:
        print(full_msg)


def ok_cancel_dialog(msg_: str, *args, **kwargs) -> bool:
    """
    Show an OK/cancel dialog, whose message is prefixed with "[PACKAGE_NAME]".

    :param      msg_:      The message
    :param      args:      The arguments for `str.format`
    :param      kwargs:    The keywords arguments for `str.format`
    """
    return sublime.ok_cancel_dialog("[{}] {}".format(PACKAGE_NAME, msg_.format(*args, **kwargs)))


def prepare_completion_request(view: sublime.View) -> Optional[Dict[str, Any]]:
    sel = view.sel()
    if len(sel) != 1:
        return None

    file_path = view.file_name() or ""
    row, col = view.rowcol(sel[0].begin())
    return {
        "doc": {
            "source": view.substr(sublime.Region(0, view.size())),
            "tabSize": view.settings().get("tab_size"),
            "indentSize": 1,  # there is no such concept in ST
            "insertSpaces": view.settings().get("translate_tabs_to_spaces"),
            "path": file_path,
            "uri": file_path and filename_to_uri(file_path),
            "relativePath": get_project_relative_path(file_path),
            "languageId": get_view_language_id(view),
            "position": {"line": row, "character": col},
            # Buffer Version. Generally this is handled by LSP, but we need to handle it here
            # Will need to test getting the version from LSP
            "version": 0,
        }
    }


def preprocess_completions(view: sublime.View, completions: List[CopilotPayloadCompletion]) -> None:
    """Preprocess the `completions` from "getCompletions" request."""
    # in-place de-duplication
    unique_indexes = set(
        map(
            itemgetter(0),
            unique(enumerate(completions), key=lambda pair: pair[1]["displayText"]),
        )
    )  # type: Set[int]
    for index in range(len(completions) - 1, -1, -1):
        if index not in unique_indexes:
            del completions[index]

    # inject extra information for convenience
    for completion in completions:
        completion["point"] = view.text_point(
            completion["position"]["line"],
            completion["position"]["character"],
        )
        _generate_completion_region(view, completion)


def preprocess_panel_completions(view: sublime.View, completions: List[CopilotPayloadPanelSolution]) -> None:
    """Preprocess the `completions` from "getCompletionsCycling" request."""
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


def status_message(msg_: str, *args, icon_: Optional[str] = "✈", console_: bool = False, **kwargs) -> None:
    """
    Show a status message in the status bar, whose message is prefixed with `icon` and "Copilot".

    :param      msg_:      The message
    :param      args:      The arguments for `str.format`
    :param      icon_:     The icon
    :param      console_:  Show message in console as well?
    :param      kwargs:    The keywords arguments for `str.format`
    """
    prefix = "{} ".format(icon_) if icon_ else ""
    full_msg = "{}Copilot {}".format(prefix, msg_.format(*args, **kwargs))
    sublime.status_message(full_msg)

    if console_:
        print(full_msg)


def unique(items: Iterable[T], *, key: Optional[Callable[[T], Any]] = None) -> Generator[T, None, None]:
    """
    Generate unique items from `items` by using `key` function on item as unique identifier.
    If `key` is not provided, an item itself will be used as its unique identifier.
    """
    key = key or (lambda x: x)
    seen = set()  # type: Set[int]
    for item in items:
        k = hash(key(item))
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
