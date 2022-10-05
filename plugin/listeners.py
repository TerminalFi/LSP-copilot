import re

import sublime
import sublime_plugin
from LSP.plugin.core.typing import Any, Dict, Optional, Tuple

from .plugin import CopilotPlugin
from .ui import ViewCompletionManager, ViewPanelCompletionManager
from .utils import get_copilot_view_setting, get_session_setting, set_copilot_view_setting


class ViewEventListener(sublime_plugin.ViewEventListener):
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

    def on_query_context(self, key: str, operator: int, operand: Any, match_all: bool) -> Optional[bool]:
        def test(value: Any) -> Optional[bool]:
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
            vcm = ViewCompletionManager(self.view)

            if not vcm.is_visible or len(self.view.sel()) < 1 or not vcm.current_completion:
                return test(False)

            point = self.view.sel()[0].begin()
            line = self.view.line(point)
            beginning_of_line = self.view.substr(sublime.Region(line.begin(), point))

            return test(beginning_of_line.strip() or not re.match(r"\s", vcm.current_completion["displayText"]))

        return None

    def on_post_text_command(self, command_name: str, args: Optional[Dict[str, Any]]) -> None:
        if command_name == "lsp_save":
            self._is_saving = True

        if command_name == "auto_complete":
            plugin, session = CopilotPlugin.plugin_session(self.view)

            if plugin and session and get_session_setting(session, "hook_to_auto_complete_command"):
                plugin.request_get_completions(self.view)

    def on_post_save_async(self) -> None:
        self._is_saving = False

    def on_selection_modified_async(self) -> None:
        if not self._is_modified:
            ViewCompletionManager(self.view).handle_selection_change()

        self._is_modified = False


class EventListener(sublime_plugin.EventListener):
    def on_window_command(
        self,
        window: sublime.Window,
        command_name: str,
        args: Optional[Dict[str, Any]],
    ) -> Optional[Tuple[str, Optional[Dict[str, Any]]]]:
        sheet = window.active_sheet()

        # if the user tries to close panel completion via Ctrl+W
        if isinstance(sheet, sublime.HtmlSheet) and command_name in {"close", "close_file"}:
            completion_manager = ViewPanelCompletionManager.from_sheet_id(sheet.id())
            if completion_manager:
                completion_manager.close()
                return "noop", None

        return None
