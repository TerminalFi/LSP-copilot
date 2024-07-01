from __future__ import annotations

from typing import Any

import mdpopups
import sublime

from ..constants import COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX
from ..template import load_resource_template
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
    def code_block_index(self) -> dict[str, str]:
        """Whether the panel completions is visible."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "code_block_index", {})

    @code_block_index.setter
    def code_block_index(self, value: dict[str, str]) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "code_block_index", value)

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
        self.code_block_index = {}

        if view := find_view_by_id(self.view_id):
            view.close()

    def append_conversation_entry(self, entry: CopilotPayloadConversationEntry) -> None:
        conversation_history = self.conversation
        conversation_history.append(entry)
        self.conversation = conversation_history

    def insert_code_block_index(self, index: int, code_block: str) -> None:
        code_block_index = self.code_block_index
        code_block_index[str(index)] = code_block
        self.code_block_index = code_block_index

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

    @property
    def completion_content(self) -> str:
        conversations_entries = self._synthesize()
        return load_resource_template("chat_panel.md.jinja", True).render(
            close_url=sublime.command_url(
                "copilot_conversation_close", {"window_id": self.conversation_manager.window.id()}
            ),
            delete_url=sublime.command_url(
                "copilot_conversation_destroy_shim", {"conversation_id": self.conversation_manager.conversation_id}
            ),
            sections=[
                {
                    "kind": entry["kind"],
                    "message": "".join(entry["messages"]),
                    "thumbs_up_url": sublime.command_url(
                        "copilot_conversation_rating_shim",
                        {
                            "turn_id": entry["turnId"],
                            "rating": 1,
                        },
                    ),
                    "thumbs_down_url": sublime.command_url(
                        "copilot_conversation_rating_shim",
                        {
                            "turn_id": entry["turnId"],
                            "rating": 0,
                        },
                    ),
                }
                for entry in conversations_entries
            ],
        )

    def _synthesize(self) -> list[dict[str, Any]]:
        transformed_conversation = []
        current_entry = None
        inside_code_block = False
        code_block_lines = []
        code_block_index = -1

        for entry in self.conversation_manager.conversation:
            kind = entry["kind"] if entry["kind"] == "user" else "system"
            reply = entry["reply"]
            turn_id = entry["turnId"]

            if current_entry and current_entry["kind"] == kind:
                if "```" in reply and not inside_code_block:
                    inside_code_block = True
                    code_block_index += 1
                    code_block_start = reply.index("```")
                    code_block_lines = reply[code_block_start:].splitlines(True)
                    command_url = sublime.command_url(
                        "copilot_conversation_copy_code",
                        {"window_id": self.conversation_manager.window.id(), "code_block_index": code_block_index},
                    )
                    reply = (
                        reply[:code_block_start] + f"<a href='{command_url}'>Copy</a>" + "\n\n" + code_block_lines[0]
                    )
                elif inside_code_block:
                    if "```" in reply:
                        inside_code_block = False
                        code_block_lines = []
                        self.conversation_manager.insert_code_block_index(
                            code_block_index, "".join(current_entry["code_block"])
                        )
                    else:
                        current_entry["code_block"].extend(reply)
                current_entry["messages"].append(reply)
            else:
                if current_entry:
                    transformed_conversation.append(current_entry)
                current_entry = {"kind": kind, "messages": [reply], "code_block": [], "turnId": turn_id}

        if current_entry:
            transformed_conversation.append(current_entry)

        return transformed_conversation

    def open(self) -> None:
        active_group = self.window.active_group()
        if active_group == self.window.num_groups() - 1:
            self._open_in_side_by_side(self.window)
        else:
            self._open_in_group(self.window, active_group + 1)

        self.window.focus_view(self.window.active_view())  # type: ignore

    def update(self) -> None:
        sheet = self.window.transient_sheet_in_group(self.conversation_manager.group_id)
        if not isinstance(sheet, sublime.HtmlSheet):
            return

        mdpopups.update_html_sheet(sheet=sheet, contents=self.completion_content, md=True, wrapper_class="wrapper")

    def close(self) -> None:
        sheet = self.window.transient_sheet_in_group(self.conversation_manager.group_id)
        if not isinstance(sheet, sublime.HtmlSheet):
            return

        sheet.close()
        self.conversation_manager.is_visible = False
        if self.conversation_manager.original_layout:
            self.window.set_layout(self.conversation_manager.original_layout)  # type: ignore
            self.conversation_manager.original_layout = None

        self.window.focus_view(self.window.active_view())  # type: ignore

    def _open_in_group(self, window: sublime.Window, group_id: int) -> None:
        self.conversation_manager.group_id = group_id

        window.focus_group(group_id)
        sheet = mdpopups.new_html_sheet(
            window=window,
            name="Copilot Chat",
            contents=self.completion_content,
            md=True,
            flags=sublime.TRANSIENT,
            wrapper_class="wrapper",
        )
        self.conversation_manager.view_id = sheet.id()

    def _open_in_side_by_side(self, window: sublime.Window) -> None:
        self.conversation_manager.original_layout = window.layout()  # type: ignore
        window.set_layout({
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
        })
        self._open_in_group(window, 1)
