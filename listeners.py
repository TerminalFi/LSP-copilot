import sublime_plugin

from .plugin import CopilotPlugin
from .ui import ViewCompletionManager
from .utils import get_copilot_view_setting, get_setting


class EventListener(sublime_plugin.ViewEventListener):
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
