from .constants import PHANTOM_KEY
import mdpopups
import os
import sublime


def clear_completion_preview(view: sublime.View) -> None:
    mdpopups.erase_phantoms(view=view, key=PHANTOM_KEY)


def get_project_relative_path(file_path: str) -> str:
    ret = ""
    for folder in sublime.active_window().folders():
        try:
            ret = min(ret, os.path.relpath(file_path, folder), key=len)
        except ValueError:
            pass
    return ret or file_path
