import functools

import sublime_plugin
from LSP.plugin.core.types import FEATURES_TIMEOUT, debounced

from .plugin import CopilotPlugin
from .ui import Completion
from .utils import get_copilot_view_setting


class EventListener(sublime_plugin.ViewEventListener):
    def on_modified_async(self) -> None:
        plugin = CopilotPlugin.plugin_from_view(self.view)
        if not plugin:
            return

        debounced(
            functools.partial(plugin.request_get_completions, self.view),
            FEATURES_TIMEOUT,
            lambda: not get_copilot_view_setting(self.view, "is_waiting", False),
            async_thread=True,
        )

    def on_deactivated_async(self) -> None:
        Completion(self.view).hide()
