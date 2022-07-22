import sublime
import sublime_plugin
from LSP.plugin.core.typing import Any, Dict, Optional, Tuple

from .plugin import CopilotPlugin
from .ui import ViewCompletionManager, ViewPanelCompletionManager
from .utils import get_setting


class ViewEventListener(sublime_plugin.ViewEventListener):
    def on_modified_async(self) -> None:
        plugin = CopilotPlugin.plugin_from_view(self.view)
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


class EventListener(sublime_plugin.EventListener):
    def on_window_command(
        self,
        window: sublime.Window,
        command_name: str,
        args: Optional[Dict[str, Any]],
    ) -> Optional[Tuple[str, Optional[Dict[str, Any]]]]:
        # if the user tries to close panel completion via Ctrl+W
        if command_name in ("close", "close_file"):
            sheet = window.active_sheet()
            if not sheet:
                return
            completion_manager = ViewPanelCompletionManager.from_sheet_id(sheet.id())
            if completion_manager and len(completion_manager.view.buffer().views()) == 1:
                completion_manager.close()
                return ("noop", None)
