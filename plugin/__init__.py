from __future__ import annotations

from .client import CopilotPlugin
from .commands import (
    CopilotAcceptCompletionCommand,
    CopilotAcceptPanelCompletionCommand,
    CopilotAcceptPanelCompletionShimCommand,
    CopilotAskCompletionsCommand,
    CopilotCheckFileStatusCommand,
    CopilotCheckStatusCommand,
    CopilotClosePanelCompletionCommand,
    CopilotConversationAgentsCommand,
    CopilotConversationChatCommand,
    CopilotConversationCopyCodeCommand,
    CopilotConversationDestroyCommand,
    CopilotConversationRatingCommand,
    CopilotConversationTemplatesCommand,
    CopilotGetPanelCompletionsCommand,
    CopilotGetVersionCommand,
    CopilotNextCompletionCommand,
    CopilotPreviousCompletionCommand,
    CopilotRejectCompletionCommand,
    CopilotSignInCommand,
    CopilotSignInWithGithubTokenCommand,
    CopilotSignOutCommand,
)
from .listeners import EventListener, ViewEventListener, copilot_ignore_observer
from .utils import CopilotIgnore, all_windows

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
    "CopilotCheckFileStatusCommand",
    "CopilotClosePanelCompletionCommand",
    "CopilotGetPanelCompletionsCommand",
    "CopilotGetVersionCommand",
    "CopilotNextCompletionCommand",
    "CopilotPreviousCompletionCommand",
    "CopilotRejectCompletionCommand",
    "CopilotSignInCommand",
    "CopilotSignInWithGithubTokenCommand",
    "CopilotSignOutCommand",
    "CopilotConversationChatCommand",
    "CopilotConversationDestroyCommand",
    "CopilotConversationAgentsCommand",
    "CopilotConversationTemplatesCommand",
    "CopilotConversationRatingCommand",
    "CopilotConversationCopyCodeCommand",
    # ST: event listeners
    "EventListener",
    "ViewEventListener",
)


def plugin_loaded() -> None:
    """Executed when this plugin is loaded."""
    CopilotPlugin.setup()
    copilot_ignore_observer.setup()
    for window in all_windows():
        CopilotIgnore(window).load_patterns()


def plugin_unloaded() -> None:
    """Executed when this plugin is unloaded."""
    CopilotPlugin.window_attrs.clear()
    CopilotPlugin.cleanup()
    CopilotIgnore.cleanup()
    if copilot_ignore_observer:
        copilot_ignore_observer.cleanup()
