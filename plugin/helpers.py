from __future__ import annotations

import itertools
import os
import re
import threading
import time
from operator import itemgetter
from pathlib import Path
from typing import Any, Callable, Literal, Sequence

import sublime
from LSP.plugin.core.url import filename_to_uri
from more_itertools import duplicates_everseen, first_true
from wcmatch import glob

from .constants import COPILOT_WINDOW_SETTINGS_PREFIX, PACKAGE_NAME
from .log import log_error
from .settings import get_plugin_setting_dotted
from .types import (
    CopilotPayloadCompletion,
    CopilotPayloadPanelSolution,
    CopilotUserDefinedPromptTemplates,
)
from .utils import (
    all_views,
    all_windows,
    drop_falsy,
    erase_copilot_setting,
    erase_copilot_view_setting,
    get_copilot_setting,
    get_project_relative_path,
    get_view_language_id,
    set_copilot_setting,
    simple_urlopen,
)


class ActivityIndicator:
    def __init__(self, callback: Callable[[dict[str, Any]], None] | None = None) -> None:
        self.thread: threading.Thread | None = None
        self.animation = ["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"]  # taken from Package Control
        self.animation_cycled = itertools.cycle(self.animation)
        self.callback = callback
        self.stop_event = threading.Event()

    def start(self) -> None:
        if not (self.thread and self.thread.is_alive()):
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop(self) -> None:
        if self.thread:
            self.stop_event.set()
            self.thread.join()
            if self.callback:
                self.callback({"is_waiting": ""})

    def _run(self) -> None:
        while not self.stop_event.is_set():
            if self.callback:
                self.callback({"is_waiting": next(self.animation_cycled)})
            time.sleep(0.1)


class GithubInfo:
    AVATAR_PATH = Path(sublime.cache_path()) / f"{PACKAGE_NAME}/avatar.png"
    AVATAR_RESOURCE_URL = f"res://Cache/{PACKAGE_NAME}/avatar.png"

    @classmethod
    def get_avatar_img_src(cls) -> str:
        if cls.AVATAR_PATH.is_file():
            return cls.AVATAR_RESOURCE_URL
        return ""

    @classmethod
    def fetch_avatar(cls, username: str, *, size: int = 64) -> None:
        """If there is no cached avatar, fetches the avatar from GitHub and saves it to the cache."""
        if not username:
            log_error("No username provided for fetching avatar.")
            return

        cls.update_avatar(username, size=size)

    @classmethod
    def update_avatar(cls, username: str, *, size: int = 64) -> None:
        """Updates the avatar from GitHub and saves it to the cache directory."""
        if not username:
            cls.clear_avatar()
            return

        try:
            data = simple_urlopen(f"https://github.com/{username}.png?size={size}")
        except Exception as e:
            log_error(f'Failed to fetch avatar for "{username}" because: {e}')
            cls.clear_avatar()
            return

        cls.AVATAR_PATH.parent.mkdir(parents=True, exist_ok=True)
        cls.AVATAR_PATH.write_bytes(data)

    @classmethod
    def clear_avatar(cls) -> None:
        cls.AVATAR_PATH.unlink(missing_ok=True)


class CopilotIgnore:
    def __init__(self, window: sublime.Window) -> None:
        self.window = window
        self.patterns: dict[str, list[str]] = {}
        self.load_patterns()

    @classmethod
    def cleanup(cls) -> None:
        for window in all_windows():
            erase_copilot_setting(window, COPILOT_WINDOW_SETTINGS_PREFIX, "copilotignore.patterns")
        for view in all_views():
            erase_copilot_view_setting(view, "is_copilot_ignored")

    def unload_patterns(self) -> None:
        self.patterns.clear()
        erase_copilot_setting(self.window, COPILOT_WINDOW_SETTINGS_PREFIX, "copilotignore.patterns")

    def load_patterns(self) -> None:
        self.patterns.clear()

        # Load workspace patterns
        for folder in self.window.folders():
            self.add_patterns_from_file(os.path.join(folder, ".copilotignore"), folder)

        set_copilot_setting(self.window, COPILOT_WINDOW_SETTINGS_PREFIX, "copilotignore.patterns", self.patterns)

    def read_ignore_patterns(self, file_path: str) -> list[str]:
        if os.path.isfile(file_path):
            with open(file_path, encoding="utf-8") as f:
                return list(drop_falsy(map(str.strip, f)))
        return []

    def add_patterns_from_file(self, file_path: str, folder: str) -> None:
        if patterns := self.read_ignore_patterns(file_path):
            self.patterns[folder] = patterns

    def matches_any_pattern(self, file_path: str | Path) -> bool:
        file_path = Path(file_path)
        loaded_patterns: dict[str, list[str]] = get_copilot_setting(
            self.window,
            COPILOT_WINDOW_SETTINGS_PREFIX,
            "copilotignore.patterns",
            self.patterns,
        )
        for folder, patterns in loaded_patterns.items():
            try:
                relative_path = file_path.relative_to(folder).as_posix()
            except ValueError:
                continue
            if glob.globmatch(relative_path, patterns, flags=glob.GLOBSTAR):
                return True
        return False

    def trigger(self, view: sublime.View) -> bool:
        if self.patterns and (file := view.file_name()):
            return self.matches_any_pattern(file)
        return False


def prepare_completion_request(view: sublime.View, max_selections: int = 1) -> dict[str, Any] | None:
    if not view:
        return None
    if len(sel := view.sel()) > max_selections or len(sel) == 0:
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
            "uri": file_path if file_path.startswith("buffer:") else filename_to_uri(file_path),
            "relativePath": get_project_relative_path(file_path),
            "languageId": get_view_language_id(view),
            "position": {"line": row, "character": col},
            # Buffer Version. Generally this is handled by LSP, but we need to handle it here
            # Will need to test getting the version from LSP
            "version": view.change_count(),
        }
    }


def prepare_conversation_turn_request(
    conversation_id: str, window_id: int, message: str, view: sublime.View, source: Literal["panel", "inline"] = "panel"
) -> dict[str, Any] | None:
    if not (initial_doc := prepare_completion_request(view, max_selections=5)):
        return None
    turn = {
        "conversationId": conversation_id,
        "message:": message,
        "workDoneToken": f"copilot_chat://{window_id}",
        "doc": initial_doc["doc"],
        "computeSuggestions": True,
        "references": [],
        "source": source,
    }

    visible_region = view.visible_region()
    visible_start = view.rowcol(visible_region.begin())
    visible_end = view.rowcol(visible_region.end())

    # References can technicaly be across multiple files
    # TODO: Support references across multiple files
    for selection in view.sel():
        if selection.empty() or view.substr(selection).strip() == "":
            continue
        file_path = view.file_name() or f"buffer:{view.buffer().id()}"
        selection_start = view.rowcol(selection.begin())
        selection_end = view.rowcol(selection.end())
        turn["references"].append({
            "type": "file",
            "status": "included",
            "uri": file_path if file_path.startswith("buffer:") else filename_to_uri(file_path),
            "range": initial_doc["doc"]["position"],
            "visibleRange": {
                "start": {"line": visible_start[0], "character": visible_start[1]},
                "end": {"line": visible_end[0], "character": visible_end[1]},
            },
            "selection": {
                "start": {"line": selection_start[0], "character": selection_start[1]},
                "end": {"line": selection_end[0], "character": selection_end[1]},
            },
        })
    return turn


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


def preprocess_chat_message(
    view: sublime.View,
    message: str,
    templates: Sequence[CopilotUserDefinedPromptTemplates] | None = None,
) -> tuple[bool, str]:
    from .template import load_string_template

    templates = templates or []
    user_template = first_true(templates, pred=lambda t: f"/{t['id']}" == message)
    is_template = False

    if user_template:
        is_template = True
        message += "\n\n{{ user_prompt }}\n\n{{ code }}"
        message += "\n\n{{ user_prompt }}\n\n"
    else:
        return False, message

    region = view.sel()[0]
    lang = get_view_language_id(view, region.begin())

    template = load_string_template(message)
    message = template.render(
        code=f"\n```{lang}\n{view.substr(region)}\n```\n",
        user_prompt="\n".join(user_template["prompt"]) if user_template else "",
    )

    return is_template, message


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


def preprocess_panel_completions(view: sublime.View, completions: Sequence[CopilotPayloadPanelSolution]) -> None:
    """Preprocess the `completions` from "getCompletionsCycling" request."""
    for completion in completions:
        _generate_completion_region(view, completion)


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


def is_debug_mode() -> bool:
    return bool(get_plugin_setting_dotted("settings.debug", False))
