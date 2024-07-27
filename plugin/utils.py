from __future__ import annotations

import gzip
import os
import re
import textwrap
import threading
import urllib.request
from collections.abc import Callable, Generator, Iterable
from functools import wraps
from itertools import takewhile
from operator import itemgetter
from typing import Any, TypeVar, Union, cast

import sublime
from LSP.plugin.core.sessions import Session
from LSP.plugin.core.types import basescope2languageid
from LSP.plugin.core.url import filename_to_uri
from more_itertools import duplicates_everseen, first_true

from .constants import COPILOT_VIEW_SETTINGS_PREFIX, PACKAGE_NAME
from .types import CopilotPayloadCompletion, CopilotPayloadPanelSolution, T_Callable

_T = TypeVar("_T")
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
    return instance.settings().get(f"{prefix}.{key}", default)


def set_copilot_setting(instance: sublime.Window | sublime.View, prefix: str, key: str, default: Any = None) -> Any:
    instance.settings().set(f"{prefix}.{key}", default)


def erase_copilot_setting(instance: sublime.Window | sublime.View, prefix: str, key: str) -> Any:
    instance.settings().erase(f"{prefix}.{key}")


def get_copilot_view_setting(view: sublime.View, key: str, default: Any = None) -> Any:
    return get_copilot_setting(view, COPILOT_VIEW_SETTINGS_PREFIX, key, default)


def set_copilot_view_setting(view: sublime.View, key: str, value: Any) -> None:
    set_copilot_setting(view, COPILOT_VIEW_SETTINGS_PREFIX, key, value)


def erase_copilot_view_setting(view: sublime.View, key: str) -> None:
    erase_copilot_setting(view, COPILOT_VIEW_SETTINGS_PREFIX, key)


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
    full_msg = f"[{PACKAGE_NAME}] {msg_.format(*args, **kwargs)}"
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
    return sublime.ok_cancel_dialog(f"[{PACKAGE_NAME}] {msg_.format(*args, **kwargs)}")


def prepare_completion_request(view: sublime.View) -> dict[str, Any] | None:
    if not view:
        return None
    if len(sel := view.sel()) != 1:
        return None

    file_path = view.file_name() or f"buffer:{view.buffer().id()}"
    row, col = view.rowcol(sel[0].begin())
    return {
        "doc": {
            "source": view.substr(sublime.Region(0, view.size())),
            "tabSize": view.settings().get("tab_size"),
            "indentSize": 1,  # there is no such concept in ST
            "insertSpaces": view.settings().get("translate_tabs_to_spaces"),
            "path": file_path,
            "uri": file_path if file_path.startswith("buffer:") else file_path and filename_to_uri(file_path),
            "relativePath": get_project_relative_path(file_path),
            "languageId": get_view_language_id(view),
            "position": {"line": row, "character": col},
            # Buffer Version. Generally this is handled by LSP, but we need to handle it here
            # Will need to test getting the version from LSP
            "version": view.change_count(),
        }
    }


def preprocess_message_for_html(message: str) -> str:
    new_lines: list[str] = []
    inside_code_block = False
    inline_code_pattern = re.compile(r"`([^`]*)`")
    for line in message.split("\n"):
        if line.lstrip().startswith("```"):
            inside_code_block = not inside_code_block
            new_lines.append(line)
            continue
        if not inside_code_block:
            escaped_line = ""
            start = 0
            for match in inline_code_pattern.finditer(line):
                escaped_line += re.sub(r"<(.*?)>", r"&lt;\1&gt;", line[start : match.start()])
                escaped_line += match.group(0)
                start = match.end()
            escaped_line += re.sub(r"<(.*?)>", r"&lt;\1&gt;", line[start:])
            new_lines.append(escaped_line)
        else:
            new_lines.append(line)
    return "\n".join(new_lines)


def preprocess_completions(view: sublime.View, completions: list[CopilotPayloadCompletion]) -> None:
    """Preprocess the `completions` from "getCompletions" request."""
    # in-place de-duplication
    duplicate_indexes = list(
        map(
            itemgetter(0),  # the index from enumerate
            duplicates_everseen(enumerate(completions), key=lambda pair: pair[1]["displayText"]),
        )
    )
    # delete from the end to avoid changing the index during iteration
    for index in reversed(duplicate_indexes):
        del completions[index]

    # inject extra information for convenience
    for completion in completions:
        completion["point"] = view.text_point(
            completion["position"]["line"],
            completion["position"]["character"],
        )
        _generate_completion_region(view, completion)


def preprocess_panel_completions(view: sublime.View, completions: list[CopilotPayloadPanelSolution]) -> None:
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


def status_message(msg_: str, *args, icon_: str | None = "✈", console_: bool = False, **kwargs) -> None:
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


def _generate_completion_region(
    view: sublime.View,
    completion: CopilotPayloadCompletion | CopilotPayloadPanelSolution,
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


def find_index_by_key_value(items, key, value):
    return next((index for index, item in enumerate(items) if item.get(key) == value), -1)


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
