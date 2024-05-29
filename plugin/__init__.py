from __future__ import annotations

from .commands import (
    CopilotAcceptCompletionCommand,
    CopilotAcceptPanelCompletionCommand,
    CopilotAcceptPanelCompletionShimCommand,
    CopilotAskCompletionsCommand,
    CopilotCheckStatusCommand,
    CopilotClosePanelCompletionCommand,
    CopilotGetPanelCompletionsCommand,
    CopilotGetVersionCommand,
    CopilotNextCompletionCommand,
    CopilotPreviousCompletionCommand,
    CopilotRejectCompletionCommand,
    CopilotSignInCommand,
    CopilotSignInWithGithubTokenCommand,
    CopilotSignOutCommand,
)
from .listeners import EventListener, ViewEventListener
from .plugin import CopilotPlugin

__all__ = (
    # ST: core
    "plugin_loaded",
    "plugin_unloaded",
    # ST: commands
    "CopilotAcceptCompletionCommand",
    "CopilotAcceptPanelCompletionCommand",
    "CopilotAcceptPanelCompletionShimCommand",
    "CopilotAskCompletionsCommand",
    "CopilotCheckStatusCommand",
    "CopilotClosePanelCompletionCommand",
    "CopilotGetPanelCompletionsCommand",
    "CopilotGetVersionCommand",
    "CopilotNextCompletionCommand",
    "CopilotPreviousCompletionCommand",
    "CopilotRejectCompletionCommand",
    "CopilotSignInCommand",
    "CopilotSignInWithGithubTokenCommand",
    "CopilotSignOutCommand",
    # ST: event listeners
    "EventListener",
    "ViewEventListener",
)


def plugin_loaded() -> None:
    CopilotPlugin.setup()


def plugin_unloaded() -> None:
    CopilotPlugin.cleanup()
    CopilotPlugin.plugin_mapping.clear()
