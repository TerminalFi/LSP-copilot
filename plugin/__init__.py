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
    CopilotConversationChatShimCommand,
    CopilotConversationCloseCommand,
    CopilotConversationCopyCodeCommand,
    CopilotConversationDestroyCommand,
    CopilotConversationDestroyShimCommand,
    CopilotConversationInsertCodeCommand,
    CopilotConversationInsertCodeShimCommand,
    CopilotConversationRatingCommand,
    CopilotConversationRatingShimCommand,
    CopilotConversationTemplatesCommand,
    CopilotConversationTurnDeleteCommand,
    CopilotConversationTurnDeleteShimCommand,
    CopilotGetPanelCompletionsCommand,
    CopilotGetVersionCommand,
    CopilotNextCompletionCommand,
    CopilotPrepareAndEditSettingsCommand,
    CopilotPreviousCompletionCommand,
    CopilotRejectCompletionCommand,
    CopilotSignInCommand,
    CopilotSignInWithGithubTokenCommand,
    CopilotSignOutCommand,
    CopilotToggleConversationChatCommand,
)
from .helpers import CopilotIgnore
from .listeners import EventListener, ViewEventListener, copilot_ignore_observer
from .utils import all_windows

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
    "CopilotToggleConversationChatCommand",
    "CopilotConversationChatShimCommand",
    "CopilotConversationChatCommand",
    "CopilotConversationCloseCommand",
    "CopilotConversationDestroyShimCommand",
    "CopilotConversationDestroyCommand",
    "CopilotConversationAgentsCommand",
    "CopilotConversationTemplatesCommand",
    "CopilotConversationTurnDeleteCommand",
    "CopilotConversationTurnDeleteShimCommand",
    "CopilotConversationRatingShimCommand",
    "CopilotConversationRatingCommand",
    "CopilotConversationCopyCodeCommand",
    "CopilotConversationInsertCodeShimCommand",
    "CopilotConversationInsertCodeCommand",
    # ST: helper commands
    "CopilotPrepareAndEditSettingsCommand",
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
