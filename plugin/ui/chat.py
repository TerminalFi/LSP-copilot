from __future__ import annotations

import sublime
from lsp_utils._client_handler.abstract_plugin import Request, Session

from ..constants import COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, REQ_CONVERSATION_TURN
from ..types import CopilotPayloadConversationEntry, StLayout
from ..utils import (
    find_view_by_id,
    find_window_by_id,
    get_copilot_setting,
    prepare_completion_request,
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

    def __init__(self, session: Session, window: sublime.Window) -> None:
        self.window = window
        self.session = session

    def reset(self) -> None:
        self.is_waiting = False
        self.is_visible = False

    def append_conversation_entry(self, entry: CopilotPayloadConversationEntry) -> None:
        conversation_history = self.conversation
        conversation_history.append(entry)
        self.conversation = conversation_history

    @staticmethod
    def find_window_by_token_id(token_id: str) -> sublime.Window | None:
        window_id = int(remove_prefix(token_id, "copilot_chat://"))
        return find_window_by_id(window_id)

    def prompt(self):
        self.window.show_input_panel("Copilot Chat", "", self._update_conversation_panel, None, None)

    def _update_conversation_panel(self, message: str) -> None:
        self.append_conversation_entry({
            "kind": "user",
            "conversationId": self.conversation_id,
            "reply": message,
            "turnId": "user",
            "annotations": [],
            "hideText": False,
        })
        self.is_waiting = True
        view_last_active_view = find_view_by_id(self.last_active_view_id)
        self.session.send_request(
            Request(
                REQ_CONVERSATION_TURN,
                {
                    "conversationId": self.conversation_id,
                    "message": message,
                    "workDoneToken": f"copilot_chat://{self.window.id()}",  # Not sure where this comes from
                    "doc": prepare_completion_request(view_last_active_view)["doc"],
                    "computeSuggestions": True,
                    "references": [],
                    "source": "panel",
                },
            ),
            self.prompt(),
        )
        self.update()

    def open(self, *, completion_target_count: int | None = None) -> None:
        _ConversationEntry(self.session, self.window).open()

    def update(self) -> None:
        """Update the completion panel."""
        _ConversationEntry(self.session, self.window).update()
        self.prompt()

    def close(self) -> None:
        """Close the completion panel."""
        _ConversationEntry(self.session, self.window).close()


class _ConversationEntry:
    def __init__(self, session: Session, window: sublime.Window) -> None:
        self.window = window
        self.conversation_manager = WindowConversationManager(session, window)

    @property
    def conversation_content(self) -> str:
        conversation_lines = []
        for entry in self.conversation_manager.conversation:
            if entry["kind"] == "user":
                conversation_lines.append(f"user: {entry['reply']}")
            else:
                conversation_lines.append(f"system: {entry['reply']}")
        return "\n".join(conversation_lines)

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
        view.run_command("select_all")
        view.run_command("left_delete")
        view.run_command("insert", {"characters": self.conversation_content})
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
        view.set_name("Copilot Chat")
        view.set_scratch(False)
        # erase view
        view.run_command("select_all")
        view.run_command("left_delete")
        view.run_command("insert", {"characters": self.conversation_content})
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
