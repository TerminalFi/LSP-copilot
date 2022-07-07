from .plugin import CopilotPlugin
from .utils import get_view_is_waiting_completion
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
            lambda: not get_view_is_waiting_completion(self.view),
            async_thread=True,
        )
