from .constants import COPILOT_WAITING_COMPLETION_KEY
from .plugin import CopilotPlugin
from LSP.plugin.core.types import debounced
from LSP.plugin.core.types import FEATURES_TIMEOUT
import functools
import sublime_plugin


class EventListener(sublime_plugin.ViewEventListener):
    def on_modified_async(self) -> None:
        plugin = CopilotPlugin.plugin_from_view(self.view)
        if not plugin:
            return
        debounced(
            functools.partial(plugin.request_get_completions, self.view),
            FEATURES_TIMEOUT,
            lambda: not getattr(self.view, COPILOT_WAITING_COMPLETION_KEY, False),
            async_thread=True,
        )
