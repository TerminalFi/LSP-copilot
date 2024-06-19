from __future__ import annotations

import re
from collections.abc import Callable
from functools import wraps
from typing import Any, cast

import sublime
import sublime_plugin

from .client import CopilotPlugin
from .types import T_Callable
from .ui import ViewCompletionManager, ViewPanelCompletionManager
from .utils import get_copilot_view_setting, get_session_setting, is_active_view, set_copilot_view_setting


def _must_be_active_view(*, failed_return: Any = None) -> Callable[[T_Callable], T_Callable]:
    def decorator(func: T_Callable) -> T_Callable:
        @wraps(func)
        def wrapped(self: Any, *arg, **kwargs) -> Any:
            if is_active_view(self.view):
                return func(self, *arg, **kwargs)
            return failed_return

        return cast(T_Callable, wrapped)

    return decorator


class ViewEventListener(sublime_plugin.ViewEventListener):
    @classmethod
    def applies_to_primary_view_only(cls) -> bool:
        # To fix "https://github.com/TerminalFi/LSP-copilot/issues/102",
        # let cloned views trigger their event listeners too.
        # But we guard some of event listeners only work for the activate view.
        return False

    @property
    def _is_modified(self) -> bool:
        return get_copilot_view_setting(self.view, "_is_modified", False)

    @_is_modified.setter
    def _is_modified(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "_is_modified", value)

    @property
    def _is_saving(self) -> bool:
        return get_copilot_view_setting(self.view, "_is_saving", False)

    @_is_saving.setter
    def _is_saving(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "_is_saving", value)

    @_must_be_active_view()
    def on_modified_async(self) -> None:
        self._is_modified = True

        plugin, session = CopilotPlugin.plugin_session(self.view)
        if not plugin or not session:
            return

        vcm = ViewCompletionManager(self.view)
        vcm.handle_text_change()

        if not self._is_saving and get_session_setting(session, "auto_ask_completions") and not vcm.is_waiting:
            plugin.request_get_completions(self.view)

    def on_deactivated_async(self) -> None:
        ViewCompletionManager(self.view).hide()

    def on_pre_close(self) -> None:
        # close corresponding panel completion
        ViewPanelCompletionManager(self.view).close()

    def on_close(self) -> None:
        ViewCompletionManager(self.view).handle_close()

    def on_query_context(self, key: str, operator: int, operand: Any, match_all: bool) -> bool | None:
        def test(value: Any) -> bool | None:
            if operator == sublime.OP_EQUAL:
                return value == operand
            if operator == sublime.OP_NOT_EQUAL:
                return value != operand
            return None

        if key == "copilot.has_signed_in":
            return test(CopilotPlugin.get_account_status().has_signed_in)

        if key == "copilot.is_authorized":
            return test(CopilotPlugin.get_account_status().is_authorized)

        if key == "copilot.is_on_completion":
            if not (
                (vcm := ViewCompletionManager(self.view)).is_visible
                and len(self.view.sel()) >= 1
                and vcm.current_completion
            ):
                return test(False)

            point = self.view.sel()[0].begin()
            line = self.view.line(point)
            beginning_of_line = self.view.substr(sublime.Region(line.begin(), point))

            return test(beginning_of_line.strip() != "" or not re.match(r"\s", vcm.current_completion["displayText"]))

        plugin, session = CopilotPlugin.plugin_session(self.view)
        if not plugin or not session:
            return None

        if key == "copilot.commit_completion_on_tab":
            return test(get_session_setting(session, "commit_completion_on_tab"))

        return None

    def on_post_text_command(self, command_name: str, args: dict[str, Any] | None) -> None:
        if command_name == "lsp_save":
            self._is_saving = True

        if command_name == "auto_complete":
            plugin, session = CopilotPlugin.plugin_session(self.view)
            if plugin and session and get_session_setting(session, "hook_to_auto_complete_command"):
                plugin.request_get_completions(self.view)

    def on_post_save_async(self) -> None:
        self._is_saving = False

    @_must_be_active_view()
    def on_selection_modified_async(self) -> None:
        if not self._is_modified:
            ViewCompletionManager(self.view).handle_selection_change()

        self._is_modified = False


class EventListener(sublime_plugin.EventListener):
    def on_window_command(
        self,
        window: sublime.Window,
        command_name: str,
        args: dict[str, Any] | None,
    ) -> tuple[str, dict[str, Any] | None] | None:
        sheet = window.active_sheet()

        # if the user tries to close panel completion via Ctrl+W
        if isinstance(sheet, sublime.HtmlSheet) and command_name in {"close", "close_file"}:
            completion_manager = ViewPanelCompletionManager.from_sheet_id(sheet.id())
            if completion_manager:
                completion_manager.close()
                return "noop", None

        return None
