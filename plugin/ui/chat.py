from __future__ import annotations

import sublime

from ..constants import COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX
from ..types import CopilotPayloadConversationEntry, StLayout
from ..utils import (
    find_view_by_id,
    find_window_by_id,
    get_copilot_setting,
    remove_prefix,
    set_copilot_setting,
)


class WindowConversationManager:
    # ------------- #
    # window settings #
    # ------------- #

    @property
    def is_visible(self) -> bool:
        """Whether the panel completions is visible."""
        return get_copilot_setting(
            self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "is_visible_conversation", False
        )

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "is_visible_conversation", value)

    @property
    def group_id(self) -> int:
        """The ID of the group which is used to show panel completions."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "view_group_id", -1)

    @group_id.setter
    def group_id(self, value: int) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "view_group_id", value)

    @property
    def last_active_view_id(self) -> int:
        """The ID of the group which is used to show panel completions."""
        return get_copilot_setting(
            self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "view_last_active_view_id", -1
        )

    @last_active_view_id.setter
    def last_active_view_id(self, value: int) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "view_last_active_view_id", value)

    @property
    def original_layout(self) -> StLayout | None:
        """The original window layout prior to panel presentation."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "original_layout", None)

    @original_layout.setter
    def original_layout(self, value: StLayout | None) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "original_layout", value)

    @property
    def view_id(self) -> int:
        """The ID of the sheet which is used to show panel completions."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "view_id", -1)

    @view_id.setter
    def view_id(self, value: int) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "view_id", value)

    @property
    def conversation_id(self) -> str:
        """Whether the panel completions is visible."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "conversation_id", "")

    @conversation_id.setter
    def conversation_id(self, value: str) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "conversation_id", value)

    @property
    def is_waiting(self) -> bool:
        """Whether the converation completions is streaming."""
        return get_copilot_setting(
            self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "is_waiting_conversation", False
        )

    @is_waiting.setter
    def is_waiting(self, value: bool) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "is_waiting_conversation", value)

    @property
    def conversation(self) -> list[CopilotPayloadConversationEntry]:
        """All `conversation` in the view. Note that this is a copy."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "conversation_entries", [])

    @conversation.setter
    def conversation(self, value: list[CopilotPayloadConversationEntry]) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "conversation_entries", value)

    # -------------- #
    # normal methods #
    # -------------- #

    def __init__(self, window: sublime.Window) -> None:
        self.window = window

    def reset(self) -> None:
        self.is_waiting = False
        self.is_visible = False
        self.original_layout = None
        self.conversation_id = ""
        self.conversation = []
        if view := find_view_by_id(self.view_id):
            view.close()

    def append_conversation_entry(self, entry: CopilotPayloadConversationEntry) -> None:
        conversation_history = self.conversation
        conversation_history.append(entry)
        self.conversation = conversation_history

    @staticmethod
    def find_window_by_token_id(token_id: str) -> sublime.Window | None:
        window_id = int(remove_prefix(token_id, "copilot_chat://"))
        return find_window_by_id(window_id)

    def prompt(self, callback):
        self.window.show_input_panel("Copilot Chat", "", callback, None, None)

    def open(self, *, completion_target_count: int | None = None) -> None:
        _ConversationEntry(self.window).open()

    def update(self) -> None:
        """Update the completion panel."""
        _ConversationEntry(self.window).update()

    def close(self) -> None:
        """Close the completion panel."""
        _ConversationEntry(self.window).close()


class _ConversationEntry:
    def __init__(self, window: sublime.Window) -> None:
        self.window = window
        self.conversation_manager = WindowConversationManager(window)

    def conversation_content(self, all: bool) -> str:
        conversation_lines = []
        previous_kind = None

        for entry in self.conversation_manager.conversation:
            current_kind = entry["kind"]
            # Adjust kind for "report"
            if current_kind == "report":
                current_kind = "system"

            if current_kind != previous_kind:
                prefix = f"{current_kind}: "
            else:
                prefix = ""
            entry = entry["reply"]
            if current_kind == "system" and entry.startswith("```"):
                entry = f"\n{entry}\n"
            conversation_lines.append(f"{prefix}{entry}\n")
            previous_kind = current_kind
        if not all and len(conversation_lines) > 0:
            return conversation_lines[-1]
        return "".join(conversation_lines)

    def open(self) -> None:
        active_group = self.window.active_group()
        if active_group == self.window.num_groups() - 1:
            self._open_in_side_by_side(self.window)
        else:
            self._open_in_group(self.window, active_group + 1)

        self.window.focus_view(self.window.active_view())  # type: ignore

    def update(self) -> None:
        if not (view := find_view_by_id(self.conversation_manager.view_id)):
            return
        view.set_read_only(False)
        view.run_command("move_to", {"to": "eof"})
        view.run_command("append", {"characters": self.conversation_content(all=False)})
        view.set_read_only(True)

    def close(self) -> None:
        if not (view := find_view_by_id(self.conversation_manager.view_id)):
            return
        view.close()
        self.conversation_manager.is_visible = False
        if self.conversation_manager.original_layout:
            self.window.set_layout(self.conversation_manager.original_layout)  # type: ignore
            self.conversation_manager.original_layout = None

        self.window.focus_view(self.window.active_view())  # type: ignore

    def _open_in_group(self, window: sublime.Window, group_id: int) -> None:
        self.conversation_manager.group_id = group_id

        window.focus_group(group_id)
        view = window.new_file()
        view.set_syntax_file("Packages/Markdown/Markdown.sublime-syntax")
        view.set_name("Copilot Chat")
        view.set_read_only(False)
        view.set_scratch(True)
        view.run_command("move_to", {"to": "eof"})
        view.run_command("insert", {"characters": self.conversation_content(all=True)})
        view.set_read_only(True)
        self.conversation_manager.view_id = view.id()

    def _open_in_side_by_side(self, window: sublime.Window) -> None:
        self.conversation_manager.original_layout = window.layout()  # type: ignore
        window.set_layout({
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
        })
        self._open_in_group(window, 1)
