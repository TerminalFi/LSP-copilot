from __future__ import annotations

import sublime

from ..types import CopilotPayloadConversationEntry
from ..utils import (
    get_copilot_view_setting,
    set_copilot_view_setting,
)


class ViewConversationManager:
    # ------------- #
    # view settings #
    # ------------- #

    @property
    def is_visible(self) -> bool:
        """Whether the panel completions is visible."""
        return get_copilot_view_setting(self.view, "is_visible_conversation", False)

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "is_visible_conversation", value)

    @property
    def conversation_id(self) -> str:
        """Whether the panel completions is visible."""
        return get_copilot_view_setting(self.view, "conversation_id", "")

    @conversation_id.setter
    def conversation_id(self, value: str) -> None:
        set_copilot_view_setting(self.view, "conversation_id", value)

    @property
    def is_waiting(self) -> bool:
        """Whether the converation completions is streaming."""
        return get_copilot_view_setting(self.view, "is_waiting_conversation", False)

    @is_waiting.setter
    def is_waiting(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "is_waiting_conversation", value)

    @property
    def completions(self) -> list[CopilotPayloadConversationEntry]:
        """All `completions` in the view. Note that this is a copy."""
        return get_copilot_view_setting(self.view, "conversation_entries", [])

    @completions.setter
    def completions(self, value: list[CopilotPayloadConversationEntry]) -> None:
        set_copilot_view_setting(self.view, "conversation_entries", value)

    # -------------- #
    # normal methods #
    # -------------- #

    def __init__(self, view: sublime.View) -> None:
        self.view = view
        self.conversation_history = []

    def reset(self) -> None:
        self.is_waiting = False
        self.is_visible = False

    def append_conversation_entry(self, entry: CopilotPayloadConversationEntry) -> None:
        conversation_history = self.conversation_history
        conversation_history.append(entry)
        self.conversation_history = conversation_history
