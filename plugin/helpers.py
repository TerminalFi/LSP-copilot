from __future__ import annotations

import itertools
import os
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import sublime
from wcmatch import glob

from .constants import COPILOT_WINDOW_SETTINGS_PREFIX, PACKAGE_NAME
from .log import log_error
from .utils import (
    all_views,
    all_windows,
    bytes_to_data_url,
    drop_falsy,
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
    AVATAR_PATH = Path(sublime.cache_path()) / f"{PACKAGE_NAME}/avatar.png"

    avatar_bytes = b""
    avatar_data_url = ""

    @classmethod
    def load_avatar_cache(cls) -> bool:
        """Loads the avatar from the cache directory. Returns successful or not."""
        try:
            cls.avatar_bytes = cls.AVATAR_PATH.read_bytes()
            cls.avatar_data_url = bytes_to_data_url(cls.avatar_bytes, mime_type="image/png")
        except FileNotFoundError:
            return False
        return True

    @classmethod
    def fetch_avatar(cls, username: str, *, size: int = 64) -> None:
        """If there is no cached avatar, fetches the avatar from GitHub and saves it to the cache."""
        if not username:
            log_error("No username provided for fetching avatar.")
            return

        if not cls.avatar_bytes and cls.load_avatar_cache():
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
        cls.load_avatar_cache()

    @classmethod
    def clear_avatar(cls) -> None:
        cls.avatar_bytes = b""
        cls.avatar_data_url = ""

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
