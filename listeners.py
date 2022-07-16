import functools

import sublime_plugin
from LSP.plugin.core.types import FEATURES_TIMEOUT, debounced

from .plugin import CopilotPlugin
from .ui import Completion


class EventListener(sublime_plugin.ViewEventListener):
    COPILOT_SUGGESTION_VISIBLE = "copilot_suggestion_visible"

    def on_modified_async(self) -> None:
        plugin = CopilotPlugin.plugin_from_view(self.view)

        if not plugin:
            return

        debounced(
            functools.partial(plugin.request_get_completions, self.view),
            FEATURES_TIMEOUT,
            lambda: not plugin.is_waiting_completion(self.view),
            async_thread=True,
        )

    def on_deactivated_async(self) -> None:
        Completion(self.view).hide()
