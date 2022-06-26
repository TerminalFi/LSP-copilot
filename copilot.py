from .plugin.core.copilot import copilot

from .plugin.core.registry import CopilotTextChangeListener
from .plugin.core.registry import CopilotViewEventListener
from .plugin.core.registry import CopilotTextCommand

from .plugin.session import CopilotEnableCommand
from .plugin.session import CopilotPreviewCompletionsCommand

def plugin_loaded():
    pass


def plugin_unloaded():
    pass
