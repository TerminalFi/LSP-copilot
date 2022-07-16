import os
import textwrap

import sublime
from LSP.plugin.core.typing import Any, Optional

from .constants import COPILOT_VIEW_SETTINGS_PREFIX


def get_copilot_view_setting(view: sublime.View, key: str, default: Optional[Any] = None) -> Any:
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


def reformat(text: str) -> str:
    """Remove common indentations and then trim."""
    return textwrap.dedent(text).strip()
