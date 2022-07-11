from .constants import COPILOT_WAITING_COMPLETION_KEY
from LSP.plugin.core.typing import Callable
import mdpopups
import os
import sublime


def clear_completion_preview(view: sublime.View) -> None:
    mdpopups.hide_popup(view)


def update_completion_preview(
    view: sublime.View,
    region: sublime.Region,
    content: str,
    on_navigate: Callable[[str], None],
    layout: int = sublime.LAYOUT_INLINE,
    md: bool = True,
    **kwargs
) -> None:
    clear_completion_preview(view)
    mdpopups.show_popup(
        view=view,
        region=region,
        content=content,
        md=md,
        on_navigate=on_navigate,
        layout=layout,
        flags=sublime.COOPERATE_WITH_AUTO_COMPLETE,
        max_width=640,
        **kwargs
    )


def get_view_is_waiting_completion(view: sublime.View) -> bool:
    return bool(getattr(view, COPILOT_WAITING_COMPLETION_KEY, False))


def set_view_is_waiting_completion(view: sublime.View, is_waiting: bool) -> None:
    setattr(view, COPILOT_WAITING_COMPLETION_KEY, is_waiting)


def get_project_relative_path(file_path: str) -> str:
    ret = file_path
    for folder in sublime.active_window().folders():
        try:
            ret = min(ret, os.path.relpath(file_path, folder), key=len)
        except ValueError:
            pass
    return ret
