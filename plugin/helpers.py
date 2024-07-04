from __future__ import annotations

import itertools
import os
import threading
import time
from collections.abc import Callable
from typing import Any

import sublime
from wcmatch import glob

from .constants import COPILOT_WINDOW_SETTINGS_PREFIX
from .utils import (
    all_views,
    bytes_to_data_url,
    erase_copilot_setting,
    erase_copilot_view_setting,
    get_copilot_setting,
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
    avatar_bytes = b""
    avatar_data_url = ""

    @classmethod
    def fetch_avatar(cls, username: str, *, size: int = 64) -> None:
        if username:
            cls.avatar_bytes = simple_urlopen(f"https://github.com/{username}.png?size={size}")
            cls.avatar_data_url = bytes_to_data_url(cls.avatar_bytes, mime_type="image/png")
        else:
            cls.avatar_bytes = b""
            cls.avatar_data_url = ""


class CopilotIgnore:
    def __init__(self, window: sublime.Window):
        self.window = window
        self.patterns: dict[str, list[str]] = {}
        self.load_patterns()

    @classmethod
    def cleanup(cls):
        for window in sublime.windows():
            erase_copilot_setting(window, COPILOT_WINDOW_SETTINGS_PREFIX, "copilotignore.patterns")
        for view in all_views():
            erase_copilot_view_setting(view, "is_copilot_ignored")

    def unload_patterns(self):
        self.patterns.clear()
        erase_copilot_setting(self.window, COPILOT_WINDOW_SETTINGS_PREFIX, "copilotignore.patterns")

    def load_patterns(self):
        self.patterns = {}

        # Load workspace patterns
        for folder in self.window.folders():
            self.add_patterns_from_file(os.path.join(folder, ".copilotignore"), folder)

        set_copilot_setting(self.window, COPILOT_WINDOW_SETTINGS_PREFIX, "copilotignore.patterns", self.patterns)

    def read_ignore_patterns(self, filepath: str):
        if os.path.exists(filepath):
            with open(filepath) as file:
                patterns = [line.strip() for line in file if line.strip()]
            return patterns
        return []

    def add_patterns_from_file(self, filepath: str, folder: str):
        patterns = self.read_ignore_patterns(filepath)
        if patterns:
            self.patterns[folder] = patterns

    def matches_any_pattern(self, file_path: str) -> bool:
        loaded_patterns = get_copilot_setting(
            self.window, COPILOT_WINDOW_SETTINGS_PREFIX, "copilotignore.patterns", self.patterns
        )
        for folder, patterns in loaded_patterns.items():
            if file_path.startswith(folder):
                relative_path = os.path.relpath(file_path, folder)
                if glob.globmatch(relative_path, patterns, flags=glob.GLOBSTAR):
                    return True
        return False

    def trigger(self, view: sublime.View):
        if not self.patterns:
            return False

        file = view.file_name()
        if not file:
            return False

        return self.matches_any_pattern(file)
