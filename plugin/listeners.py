import sublime
import sublime_plugin
from LSP.plugin.core.typing import Any, Dict, Optional, Tuple

from .plugin import CopilotPlugin
from .ui import ViewCompletionManager, ViewPanelCompletionManager
from .utils import get_setting


class ViewEventListener(sublime_plugin.ViewEventListener):
    def on_modified_async(self) -> None:
        plugin = CopilotPlugin.from_view(self.view)
        if not plugin:
            return

        session = plugin.weaksession()
        if not session:
            return

        if get_setting(session, "auto_ask_completions"):
            self.view.run_command("copilot_ask_completions")

    def on_deactivated_async(self) -> None:
        ViewCompletionManager(self.view).hide()

    def on_pre_close(self) -> None:
        # close corresponding panel completion
        ViewPanelCompletionManager(self.view).close()

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
        return None


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
                return ("noop", None)
