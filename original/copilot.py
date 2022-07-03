from .src.core.copilot import copilot

from .src.core.registry import CopilotTextChangeListener
from .src.core.registry import CopilotViewEventListener
from .src.core.registry import CopilotTextCommand

from .src.session import CopilotEnableCommand
from .src.session import CopilotSignInCommand
from .src.session import CopilotPreviewCompletionsCommand

def plugin_loaded():
    pass


def plugin_unloaded():
    pass
