import sublime
from .plugin import CopilotPlugin
from .ui import Completion
from LSP.plugin.core.types import debounced
from LSP.plugin.core.types import FEATURES_TIMEOUT
import functools
import sublime_plugin


class EventListener(sublime_plugin.ViewEventListener):
    COPILOT_SUGGESTION_VISIBLE = 'copilot_suggestion_visible'

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

    def on_query_context(self, key: str, operator: str, operand, _):
        if key != self.COPILOT_SUGGESTION_VISIBLE:
            return None

        completion = Completion(self.view)

        if operator == sublime.OP_EQUAL:
            return completion.is_visible() == operand
        elif operator == sublime.OP_NOT_EQUAL:
            return completion.is_visible() != operand
