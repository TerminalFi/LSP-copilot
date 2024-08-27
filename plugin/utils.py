from __future__ import annotations

import contextlib
import gzip
import os
import threading
import urllib.request
from collections.abc import Callable, Generator, Iterable
from functools import wraps
from itertools import takewhile
from typing import Any, Mapping, Sequence, TypeVar, Union, cast

import sublime
from LSP.plugin.core.sessions import Session
from LSP.plugin.core.types import basescope2languageid
from more_itertools import first, first_true

from .constants import COPILOT_VIEW_SETTINGS_PREFIX, PACKAGE_NAME
from .types import T_Callable

_T = TypeVar("_T")
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_T_Number = TypeVar("_T_Number", bound=Union[int, float])

all_windows = sublime.windows


def all_views(
    window: sublime.Window | None = None,
    *,
    include_transient: bool = False,
) -> Generator[sublime.View, None, None]:
    windows = [window] if window else all_windows()
    for window in windows:
        yield from window.views(include_transient=include_transient)


def all_sheets(
    window: sublime.Window | None = None,
    *,
    include_transient: bool = False,
) -> Generator[sublime.Sheet, None, None]:
    windows = [window] if window else all_windows()
    for window in windows:
        if include_transient:
            yield from drop_falsy(map(window.transient_sheet_in_group, range(window.num_groups())))
        yield from window.sheets()


def clamp(val: _T_Number, min_val: _T_Number | None = None, max_val: _T_Number | None = None) -> _T_Number:
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

            timer: threading.Timer | None = getattr(debounced, "_timer", None)
            if timer is not None:
                timer.cancel()

            timer = threading.Timer(time_s, call_function)
            timer.start()
            setattr(debounced, "_timer", timer)

        setattr(debounced, "_timer", None)
        return cast(T_Callable, debounced)

    return decorator


def drop_falsy(iterable: Iterable[_T | None]) -> Generator[_T, None, None]:
    """Drops falsy values from the iterable."""
    yield from filter(None, iterable)


def find_sheet_by_id(id: int) -> sublime.Sheet | None:
    return first_true(all_sheets(include_transient=True), pred=lambda sheet: sheet.id() == id)


def find_view_by_id(id: int) -> sublime.View | None:
    return first_true(all_views(include_transient=True), pred=lambda view: view.id() == id)


def find_window_by_id(id: int) -> sublime.Window | None:
    return first_true(all_windows(), pred=lambda window: window.id() == id)


def is_active_view(obj: Any) -> bool:
    return bool(obj and obj == sublime.active_window().active_view())


def fix_completion_syntax_highlight(view: sublime.View, point: int, code: str) -> str:
    if view.match_selector(point, "source.php"):
        return f"<?php\n{code}"
    return code


def get_copilot_setting(instance: sublime.Window | sublime.View, prefix: str, key: str, default: Any = None) -> Any:
    """Gets the Copilot-related window setting. Note that what you get is just a "copy" of the value."""
    return instance.settings().get(f"{prefix}.{key}", default)


def set_copilot_setting(instance: sublime.Window | sublime.View, prefix: str, key: str, default: Any = None) -> Any:
    instance.settings().set(f"{prefix}.{key}", default)


def erase_copilot_setting(instance: sublime.Window | sublime.View, prefix: str, key: str) -> Any:
    instance.settings().erase(f"{prefix}.{key}")


def get_copilot_view_setting(view: sublime.View, key: str, default: Any = None) -> Any:
    """Gets the Copilot-related view setting. Note that what you get is just a "copy" of the value."""
    return get_copilot_setting(view, COPILOT_VIEW_SETTINGS_PREFIX, key, default)


def set_copilot_view_setting(view: sublime.View, key: str, value: Any) -> None:
    set_copilot_setting(view, COPILOT_VIEW_SETTINGS_PREFIX, key, value)


def erase_copilot_view_setting(view: sublime.View, key: str) -> None:
    erase_copilot_setting(view, COPILOT_VIEW_SETTINGS_PREFIX, key)


def get_project_relative_path(path: str) -> str:
    """Get the relative path regarding the project root directory. If not possible, return the path as-is."""
    relpath = path
    for folder in sublime.active_window().folders():
        with contextlib.suppress(ValueError):
            relpath = min(relpath, os.path.relpath(path, folder), key=len)
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


def message_dialog(msg_: str, *args: Any, error_: bool = False, console_: bool = False, **kwargs: Any) -> None:
    """
    Show a message dialog, whose message is prefixed with "[PACKAGE_NAME]".

    :param      msg_:      The message
    :param      args:      The arguments for `str.format`
    :param      error_:    The error
    :param      console_:  Show message in console as well?
    :param      kwargs:    The keywords arguments for `str.format`
    """
    full_msg = f"[{PACKAGE_NAME}] {msg_.format(*args, **kwargs)}"
    messenger = sublime.error_message if error_ else sublime.message_dialog
    messenger(full_msg)

    if console_:
        print(full_msg)


@contextlib.contextmanager
def mutable_view(view: sublime.View) -> Generator[sublime.View, Any, None]:
    try:
        view.set_read_only(False)
        yield view
    finally:
        view.set_read_only(True)


def ok_cancel_dialog(msg_: str, *args: Any, **kwargs: Any) -> bool:
    """
    Show an OK/cancel dialog, whose message is prefixed with "[PACKAGE_NAME]".

    :param      msg_:      The message
    :param      args:      The arguments for `str.format`
    :param      kwargs:    The keywords arguments for `str.format`
    """
    return sublime.ok_cancel_dialog(f"[{PACKAGE_NAME}] {msg_.format(*args, **kwargs)}")


def remove_prefix(s: str, prefix: str) -> str:
    """Remove the prefix from the string. I.e., str.removeprefix in Python 3.9."""
    return s[len(prefix) :] if s.startswith(prefix) else s


def remove_suffix(s: str, suffix: str) -> str:
    """Remove the suffix from the string. I.e., str.removesuffix in Python 3.9."""
    # suffix="" should not call s[:-0]
    return s[: -len(suffix)] if suffix and s.endswith(suffix) else s


def status_message(msg_: str, *args: Any, icon_: str | None = "✈", console_: bool = False, **kwargs: Any) -> None:
    """
    Show a status message in the status bar, whose message is prefixed with `icon` and "Copilot".

    :param      msg_:      The message
    :param      args:      The arguments for `str.format`
    :param      icon_:     The icon
    :param      console_:  Show message in console as well?
    :param      kwargs:    The keywords arguments for `str.format`
    """
    prefix = f"{icon_} " if icon_ else ""
    full_msg = f"{prefix}Copilot {msg_.format(*args, **kwargs)}"
    sublime.status_message(full_msg)

    if console_:
        print(full_msg)


def find_index_by_key_value(items: Sequence[Mapping[_KT, _VT]], key: _KT, value: _VT) -> int:
    """
    Finds the index of the first map-like item in `items` whose `key` is equal to `value`.
    If not found, returns `-1`.
    """
    return first((idx for idx, item in enumerate(items) if key in item and item[key] == value), -1)


def simple_urlopen(url: str, *, chunk_size: int = 512 * 1024) -> bytes:
    """
    Opens a URL and reads the data in chunks, optionally decompressing gzip-encoded content.

    This function opens a connection to the specified URL and reads the response data in chunks
    of a specified size. If the response is gzip-encoded, it decompresses the data before returning it.

    Args:
        url (str): The URL to open.
        chunk_size (int, optional): The size of each chunk to read. Defaults to 512KB.

    Returns:
        bytes: The raw bytes of the data read from the URL. If the content was gzip-encoded,
               it is decompressed before being returned.
    """
    with urllib.request.urlopen(url) as resp:
        data = b""
        while chunk := resp.read(chunk_size):
            data += chunk
        if resp.info().get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
    return data
