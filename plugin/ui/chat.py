from __future__ import annotations

from typing import Callable, Any

import mdpopups
import sublime

from ..constants import COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, COPILOT_OUTPUT_PANEL_PREFIX
from ..helpers import GithubInfo, preprocess_message_for_html
from ..template import load_resource_template
from ..types import CopilotPayloadConversationEntry, CopilotPayloadConversationEntryTransformed, StLayout
from ..utils import find_view_by_id, find_window_by_id, get_copilot_setting, remove_prefix, set_copilot_setting


class WindowConversationManager:
    # --------------- #
    # window settings #
    # --------------- #

    @property
    def group_id(self) -> int:
        """The ID of the group which is used to show conversation panel."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "view_group_id", -1)

    @group_id.setter
    def group_id(self, value: int) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "view_group_id", value)

    @property
    def last_active_view_id(self) -> int:
        """The ID of the last active view that is not the conversation panel"""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "last_active_view_id", -1)

    @last_active_view_id.setter
    def last_active_view_id(self, value: int) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "last_active_view_id", value)

    @property
    def original_layout(self) -> StLayout | None:
        """The original window layout prior to panel presentation."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "original_layout", None)

    @original_layout.setter
    def original_layout(self, value: StLayout | None) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "original_layout", value)

    @property
    def view_id(self) -> int:
        """The ID of the sheet which is used to show conversation panel."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "view_id", -1)

    @view_id.setter
    def view_id(self, value: int) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "view_id", value)

    @property
    def suggested_title(self) -> str:
        """Suggested title of the conversation"""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "suggested_title", "")

    @suggested_title.setter
    def suggested_title(self, value: str) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "suggested_title", value)

    @property
    def follow_up(self) -> str:
        """Suggested follow up of the conversation provided by copilot."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "follow_up", "")

    @follow_up.setter
    def follow_up(self, value: str) -> None:
        # Fixes: https://github.com/TerminalFi/LSP-copilot/issues/182
        # Replaces ` with &#96; to avoid breaking the HTML
        set_copilot_setting(
            self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "follow_up", value.replace("`", "&#96;")
        )

    @property
    def conversation_id(self) -> str:
        """The conversation uuid used to identify the conversation."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "conversation_id", "")

    @conversation_id.setter
    def conversation_id(self, value: str) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "conversation_id", value)

    @property
    def code_block_index(self) -> dict[str, str]:
        """The tracking of code blocks across the conversation. Used to support Copy and Insert code commands."""
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
    def is_visible(self) -> bool:
        """Whether the converation completions is streaming."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "is_visible", False)

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "is_visible", value)

    @property
    def reference_block_state(self) -> dict[str, bool]:
        return get_copilot_setting(
            self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "reference_block_state", {}
        )

    @reference_block_state.setter
    def reference_block_state(self, value: dict[str, bool]) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "reference_block_state", value)

    @property
    def conversation(self) -> list[CopilotPayloadConversationEntry]:
        """All `conversation` in the view. Note that this is a copy."""
        return get_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "conversation_entries", [])

    @conversation.setter
    def conversation(self, value: list[CopilotPayloadConversationEntry]) -> None:
        set_copilot_setting(self.window, COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX, "conversation_entries", value)



    def __init__(self, window: sublime.Window) -> None:
        self.window = window

    def reset(self) -> None:
        """Reset all settings to their default values."""
        self.group_id = -1
        self.last_active_view_id = -1
        self.original_layout = None
        self.view_id = -1
        self.suggested_title = ""
        self.follow_up = ""
        self.conversation_id = ""
        self.code_block_index = {}
        self.is_waiting = False
        self.is_visible = False
        self.reference_block_state = {}
        self.conversation = []

    def append_conversation_entry(self, entry: CopilotPayloadConversationEntry) -> None:
        # `self.conversation` is a deepcopy of the original value
        # So if we do `self.conversation.append(entry)`, the source value won't be modified
        conversation = self.conversation
        conversation.append(entry)
        self.conversation = conversation

    def append_reference_block_state(self, turn_id: str, state: bool) -> None:
        # `self.reference_block_state` is a deepcopy of the original value
        # So if we do self.`reference_block_state[turn_id] = state`, the source value won't be modified
        reference_block_state = self.reference_block_state
        reference_block_state[turn_id] = state
        self.reference_block_state = reference_block_state

    def insert_code_block_index(self, index: int, code_block: str) -> None:
        # `self.code_block_index` is a deepcopy of the original value
        # So if we do `self.code_block_index[str(index)] = code_block_index`, the source value won't be modified
        code_block_index = self.code_block_index
        code_block_index[str(index)] = code_block
        self.code_block_index = code_block_index

    def toggle_references_block(self, turn_id: str) -> None:
        reference_block_state = self.reference_block_state
        reference_block_state[turn_id] = not reference_block_state.get(turn_id, False)
        self.reference_block_state = reference_block_state

    @staticmethod
    def find_window_by_token_id(token_id: str) -> sublime.Window | None:
        return sublime.active_window()

    def prompt(self, callback: Callable[[str], None], initial_text: str = "") -> None:
        self.window.show_input_panel("Copilot:", initial_text, callback, None, None)

    def open(self) -> None:
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
        self.wcm = WindowConversationManager(window)

    @property
    def completion_content(self) -> str:
        conversations_entries = self._synthesize()
        return load_resource_template("chat_panel.md.jinja", keep_trailing_newline=True).render(
            window_id=self.wcm.window.id(),
            is_waiting=self.wcm.is_waiting,
            avatar_img_src=GithubInfo.get_avatar_img_src(),
            suggested_title=preprocess_message_for_html(self.wcm.suggested_title),
            follow_up=preprocess_message_for_html(self.wcm.follow_up),
            follow_up_url=sublime.command_url(
                "copilot_conversation_chat_shim",
                {"window_id": self.wcm.window.id(), "message": self.wcm.follow_up},
            ),
            close_url=sublime.command_url(
                "copilot_conversation_close",
                {"window_id": self.wcm.window.id()},
            ),
            delete_url=sublime.command_url(
                "copilot_conversation_destroy_shim",
                {"conversation_id": self.wcm.conversation_id},
            ),
            sections=[
                {
                    "kind": entry["kind"],
                    "message": "".join(entry["messages"]),
                    "code_block_indices": entry["codeBlockIndices"],
                    "toggle_references_url": sublime.command_url(
                        "copilot_conversation_toggle_references_block",
                        {
                            "conversation_id": self.wcm.conversation_id,
                            "window_id": self.wcm.window.id(),
                            "turn_id": entry["turnId"],
                        },
                    ),
                    "references": [] if entry["kind"] != "report" else entry["references"],
                    "references_expanded": self.wcm.reference_block_state.get(entry["turnId"], False),
                    "turn_delete_url": sublime.command_url(
                        "copilot_conversation_turn_delete_shim",
                        {
                            "conversation_id": self.wcm.conversation_id,
                            "window_id": self.wcm.window.id(),
                            "turn_id": entry["turnId"],
                        },
                    ),
                    "thumbs_up_url": sublime.command_url(
                        "copilot_conversation_rating_shim",
                        {"turn_id": entry["turnId"], "rating": 1},
                    ),
                    "thumbs_down_url": sublime.command_url(
                        "copilot_conversation_rating_shim",
                        {"turn_id": entry["turnId"], "rating": -1},
                    ),
                }
                for entry in conversations_entries
            ],
        )

    def _synthesize(self) -> list[CopilotPayloadConversationEntryTransformed]:
        def inject_code_block_commands(reply: str, code_block_index: int) -> str:
            return f"CODE_BLOCK_COMMANDS_{code_block_index}\n\n{reply}"

        transformed_conversation: list[CopilotPayloadConversationEntryTransformed] = []
        current_entry: CopilotPayloadConversationEntryTransformed | None = None
        is_inside_code_block = False
        code_block_index = -1

        for idx, entry in enumerate(self.wcm.conversation):
            kind = entry["kind"]
            reply = entry["reply"]
            turn_id = entry["turnId"]

            if current_entry and current_entry["kind"] == kind:
                if reply.startswith("```"):
                    is_inside_code_block = not is_inside_code_block
                    if is_inside_code_block:
                        code_block_index += 1
                        current_entry["codeBlockIndices"].append(code_block_index)
                        reply = inject_code_block_commands(reply, code_block_index)
                    else:
                        self.wcm.insert_code_block_index(code_block_index, "".join(current_entry["codeBlocks"]))
                        current_entry["codeBlocks"] = []
                elif is_inside_code_block:
                    current_entry["codeBlocks"].append(reply)
                current_entry["messages"].append(reply)
            else:
                if current_entry:
                    transformed_conversation.append(current_entry)
                current_entry = {
                    "kind": kind,
                    "turnId": turn_id,
                    "messages": [reply],
                    "codeBlockIndices": [],
                    "codeBlocks": [],
                    "references": [],
                }
                if kind == "report":
                    current_entry["references"] = self.wcm.conversation[idx - 1].get("references", [])

                if reply.startswith("```") and kind == "report":
                    is_inside_code_block = True
                    code_block_index += 1
                    current_entry["codeBlockIndices"].append(code_block_index)
                    reply = inject_code_block_commands(reply, code_block_index)
                    current_entry["messages"] = [reply]

        if current_entry:
            # Fixes: https://github.com/TerminalFi/LSP-copilot/issues/187
            if is_inside_code_block:
                current_entry["messages"].append("```")
            transformed_conversation.append(current_entry)

        return transformed_conversation

    def open(self) -> None:
        self.wcm.is_visible = True
        active_group = self.window.active_group()
        if active_group == self.window.num_groups() - 1:
            self._open_in_side_by_side(self.window)
        else:
            self._open_in_group(self.window, active_group + 1)

        self.window.focus_view(self.window.active_view())  # type: ignore

    def update(self) -> None:
        if not (sheet := self.window.transient_sheet_in_group(self.wcm.group_id)):
            return

        mdpopups.update_html_sheet(sheet=sheet, contents=self.completion_content, md=True, wrapper_class="wrapper")

    def close(self) -> None:
        if not (sheet := self.window.transient_sheet_in_group(self.wcm.group_id)):
            return

        sheet.close()

        self.wcm.is_visible = False
        self.wcm.window.run_command("hide_panel")
        if self.wcm.original_layout:
            self.window.set_layout(self.wcm.original_layout)  # type: ignore
            self.wcm.original_layout = None

        if view := self.window.active_view():
            self.window.focus_view(view)

    def _open_in_group(self, window: sublime.Window, group_id: int) -> None:
        self.wcm.group_id = group_id

        window.focus_group(group_id)
        sheet = mdpopups.new_html_sheet(
            window=window,
            name="Copilot Chat",
            contents=self.completion_content,
            md=True,
            flags=sublime.TRANSIENT,
            wrapper_class="wrapper",
        )
        self.wcm.view_id = sheet.id()

    def _open_in_side_by_side(self, window: sublime.Window) -> None:
        self.wcm.original_layout = window.layout()  # type: ignore
        window.set_layout({
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
        })
        self._open_in_group(window, 1)


class _EditConversationEntry:
    """Handles UI rendering and management for edit conversations using HTML sheets."""

    def __init__(self, window: sublime.Window) -> None:
        self.window = window
        self.wecm = WindowEditConversationManager(window)

    @property
    def completion_content(self) -> str:
        """Generate the HTML content for the edit conversation sheet."""
        from ..helpers import GithubInfo, preprocess_message_for_html
        from ..template import load_resource_template

        # Get source file name if available
        source_file = ""
        if source_view := self.wecm.get_source_view():
            if file_name := source_view.file_name():
                import os
                source_file = os.path.basename(file_name)

        # Process conversation entries into sections
        sections = []
        for entry in self.wecm.conversation_entries:
            sections.append({
                "kind": entry.get("kind", "unknown"),
                "message": entry.get("reply", ""),
                "turnId": entry.get("turnId", ""),
                "thumbs_up_url": sublime.command_url(
                    "copilot_conversation_rating_shim",
                    {"turn_id": entry.get("turnId", ""), "rating": 1}
                ),
                "thumbs_down_url": sublime.command_url(
                    "copilot_conversation_rating_shim",
                    {"turn_id": entry.get("turnId", ""), "rating": -1}
                ),
                "turn_delete_url": sublime.command_url(
                    "copilot_edit_conversation_turn_delete",
                    {
                        "conversation_id": self.wecm.conversation_id,
                        "turn_id": entry.get("turnId", "")
                    }
                ),
            })

        return load_resource_template("edit_conversation.md.jinja", keep_trailing_newline=True).render(
            window_id=self.window.id(),
            is_waiting=self.wecm.is_waiting,
            avatar_img_src=GithubInfo.get_avatar_img_src(),
            source_file=source_file,
            sections=sections,
            pending_edits=self.wecm.pending_edits,
            close_url=sublime.command_url(
                "copilot_edit_conversation_close",
                {"conversation_id": self.wecm.conversation_id}
            ),
            destroy_url=sublime.command_url(
                "copilot_edit_conversation_destroy",
                {"conversation_id": self.wecm.conversation_id}
            ),
            apply_edits_url=sublime.command_url(
                "copilot_apply_edit_conversation_edits",
                {}
            ),
        )

    def open(self) -> None:
        """Open the edit conversation sheet."""
        self.wecm.is_visible = True
        active_group = self.window.active_group()
        if active_group == self.window.num_groups() - 1:
            self._open_in_side_by_side(self.window)
        else:
            self._open_in_group(self.window, active_group + 1)

        self.window.focus_view(self.window.active_view())  # type: ignore

    def update(self) -> None:
        """Update the edit conversation sheet content."""
        if not (sheet := self.window.transient_sheet_in_group(self.wecm.group_id)):
            return

        mdpopups.update_html_sheet(sheet=sheet, contents=self.completion_content, md=True, wrapper_class="wrapper")

    def close(self) -> None:
        """Close the edit conversation sheet."""
        if not (sheet := self.window.transient_sheet_in_group(self.wecm.group_id)):
            return

        sheet.close()

        self.wecm.is_visible = False
        self.wecm.window.run_command("hide_panel")
        if self.wecm.original_layout:
            self.window.set_layout(self.wecm.original_layout)  # type: ignore
            self.wecm.original_layout = None

        if view := self.window.active_view():
            self.window.focus_view(view)

    def _open_in_group(self, window: sublime.Window, group_id: int) -> None:
        """Open the edit conversation sheet in a specific group."""
        self.wecm.group_id = group_id

        window.focus_group(group_id)
        sheet = mdpopups.new_html_sheet(
            window=window,
            name="Copilot Edit",
            contents=self.completion_content,
            md=True,
            flags=sublime.TRANSIENT,
            wrapper_class="wrapper",
        )
        self.wecm.view_id = sheet.id()

    def _open_in_side_by_side(self, window: sublime.Window) -> None:
        """Open the edit conversation sheet in side-by-side layout."""
        self.wecm.original_layout = window.layout()  # type: ignore
        window.set_layout({
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
        })
        self._open_in_group(window, 1)

    def prompt_for_message(self, callback: Callable[[str], None], initial_text: str = "") -> None:
        """Show input panel for new message in edit conversation."""
        self.window.show_input_panel("Edit Conversation:", initial_text, callback, None, None)

    def add_user_message(self, message: str) -> None:
        """Add a user message to the edit conversation."""
        import uuid
        from ..helpers import preprocess_message_for_html

        self.wecm.append_conversation_entry({
            "kind": "user",
            "conversationId": self.wecm.conversation_id,
            "reply": preprocess_message_for_html(message),
            "turnId": str(uuid.uuid4()),
            "references": [],
            "annotations": [],
            "hideText": False,
            "warnings": [],
        })
        self.update()

    def add_assistant_message(self, message: str, turn_id: str | None = None) -> None:
        """Add an assistant message to the edit conversation."""
        import uuid
        from ..helpers import preprocess_message_for_html

        self.wecm.append_conversation_entry({
            "kind": "assistant",
            "conversationId": self.wecm.conversation_id,
            "reply": preprocess_message_for_html(message),
            "turnId": turn_id or str(uuid.uuid4()),
            "references": [],
            "annotations": [],
            "hideText": False,
            "warnings": [],
        })
        self.update()

    def show_waiting_state(self, waiting: bool = True) -> None:
        """Show or hide waiting state in the sheet."""
        self.wecm.is_waiting = waiting
        self.update()

    def add_pending_edit(self, edit: dict[str, Any]) -> None:
        """Add a pending edit and update the sheet."""
        self.wecm.add_pending_edit(edit)
        self.update()

    def clear_pending_edits(self) -> None:
        """Clear pending edits and update the sheet."""
        self.wecm.clear_pending_edits()
        self.update()


class WindowEditConversationManager:
    """Manager for edit conversations which have different lifecycle and requirements than chat conversations."""

    EDIT_CONVERSATION_SETTINGS_PREFIX = "copilot.window.edit_conversation"

    @property
    def conversation_id(self) -> str:
        """The edit conversation UUID used to identify the conversation."""
        return get_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "conversation_id", "")

    @conversation_id.setter
    def conversation_id(self, value: str) -> None:
        set_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "conversation_id", value)

    @property
    def group_id(self) -> int:
        """The ID of the group which is used to show edit conversation panel."""
        return get_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "group_id", -1)

    @group_id.setter
    def group_id(self, value: int) -> None:
        set_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "group_id", value)

    @property
    def view_id(self) -> int:
        """The ID of the sheet which is used to show edit conversation panel."""
        return get_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "view_id", -1)

    @view_id.setter
    def view_id(self, value: int) -> None:
        set_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "view_id", value)

    @property
    def original_layout(self) -> StLayout | None:
        """The original window layout prior to panel presentation."""
        return get_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "original_layout", None)

    @original_layout.setter
    def original_layout(self, value: StLayout | None) -> None:
        set_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "original_layout", value)

    @property
    def source_view_id(self) -> int:
        """The ID of the source view being edited."""
        return get_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "source_view_id", -1)

    @source_view_id.setter
    def source_view_id(self, value: int) -> None:
        set_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "source_view_id", value)

    @property
    def pending_edits(self) -> list[dict[str, Any]]:
        """List of pending edits that can be applied to the source view."""
        return get_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "pending_edits", [])

    @pending_edits.setter
    def pending_edits(self, value: list[dict[str, Any]]) -> None:
        set_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "pending_edits", value)

    @property
    def is_waiting(self) -> bool:
        """Whether the edit conversation is waiting for a response."""
        return get_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "is_waiting", False)

    @is_waiting.setter
    def is_waiting(self, value: bool) -> None:
        print("setting is_waiting to ", value)
        set_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "is_waiting", value)

    @property
    def is_visible(self) -> bool:
        """Whether the edit conversation panel is visible."""
        return get_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "is_visible", False)

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        set_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "is_visible", value)



    @property
    def conversation_entries(self) -> list[CopilotPayloadConversationEntry]:
        """All conversation entries for this edit conversation."""
        return get_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "conversation_entries", [])

    @conversation_entries.setter
    def conversation_entries(self, value: list[CopilotPayloadConversationEntry]) -> None:
        set_copilot_setting(self.window, self.EDIT_CONVERSATION_SETTINGS_PREFIX, "conversation_entries", value)

    def __init__(self, window: sublime.Window) -> None:
        self.window = window

    def reset(self) -> None:
        """Reset all edit conversation settings to their default values."""
        self.conversation_id = ""
        self.group_id = -1
        self.view_id = -1
        self.original_layout = None
        self.source_view_id = -1
        self.pending_edits = []
        self.is_waiting = False
        self.is_visible = False
        self.conversation_entries = []

    def append_conversation_entry(self, entry: CopilotPayloadConversationEntry) -> None:
        """Add a new conversation entry to the edit conversation."""
        entries = self.conversation_entries
        entries.append(entry)
        self.conversation_entries = entries

    def add_pending_edit(self, edit: dict[str, Any]) -> None:
        """Add a pending edit that can be applied to the source view."""
        edits = self.pending_edits
        edits.append(edit)
        self.pending_edits = edits

    def clear_pending_edits(self) -> None:
        """Clear all pending edits."""
        self.pending_edits = []

    def get_source_view(self) -> sublime.View | None:
        """Get the source view being edited, if it still exists."""
        return find_view_by_id(self.source_view_id)



    def destroy(self) -> None:
        """Destroy the edit conversation and clean up all resources."""
        if ui_entry := self.get_ui_entry():
            ui_entry.close()
        self.reset()

    def get_ui_entry(self) -> '_EditConversationEntry':
        """Get the UI entry helper for this edit conversation."""
        return _EditConversationEntry(self.window)

    def open(self) -> None:
        self.get_ui_entry().open()

    def update(self) -> None:
        """Update the completion panel."""
        self.get_ui_entry().update()

    def close(self) -> None:
        """Close the completion panel."""
        self.get_ui_entry().close()


    @staticmethod
    def find_by_conversation_id(conversation_id: str) -> 'WindowEditConversationManager | None':
        """Find an edit conversation manager by conversation ID across all windows."""
        for window in sublime.windows():
            wecm = WindowEditConversationManager(window)
            if wecm.conversation_id == conversation_id:
                return wecm
        return None
