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
    CopilotCodeReviewCommand,
    CopilotConversationAgentsCommand,
    CopilotConversationChatCommand,
    CopilotConversationChatShimCommand,
    CopilotConversationCloseCommand,
    CopilotConversationCopyCodeCommand,
    CopilotConversationDebugCommand,
    CopilotConversationDestroyCommand,
    CopilotConversationDestroyShimCommand,
    CopilotGitCommitGenerateCommand,
    CopilotConversationInsertCodeCommand,
    CopilotConversationInsertCodeShimCommand,
    CopilotConversationRatingCommand,
    CopilotConversationRatingShimCommand,
    CopilotConversationTemplatesCommand,
    CopilotConversationToggleReferencesBlockCommand,
    CopilotConversationTurnDeleteCommand,
    CopilotConversationTurnDeleteShimCommand,
    CopilotEditConversationCreateCommand,
    CopilotGetPanelCompletionsCommand,
    CopilotGetPromptCommand,
    CopilotGetVersionCommand,
    CopilotModelsCommand,
    CopilotNextCompletionCommand,
    CopilotPrepareAndEditSettingsCommand,
    CopilotPreviousCompletionCommand,
    CopilotRejectCompletionCommand,
    CopilotSendAnyRequestCommand,
    CopilotSetModelPolicyCommand,
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
    "CopilotCheckFileStatusCommand",
    "CopilotCheckStatusCommand",
    "CopilotCodeReviewCommand",
    "CopilotEditConversationCreateCommand",
    "CopilotClosePanelCompletionCommand",
    "CopilotConversationAgentsCommand",
    "CopilotConversationChatCommand",
    "CopilotConversationChatShimCommand",
    "CopilotConversationCloseCommand",
    "CopilotConversationCopyCodeCommand",
    "CopilotConversationDebugCommand",
    "CopilotConversationDestroyCommand",
    "CopilotConversationDestroyShimCommand",
    "CopilotConversationInsertCodeCommand",
    "CopilotConversationInsertCodeShimCommand",
    "CopilotConversationRatingCommand",
    "CopilotConversationRatingShimCommand",
    "CopilotConversationTemplatesCommand",
    "CopilotConversationToggleReferencesBlockCommand",
    "CopilotConversationTurnDeleteCommand",
    "CopilotConversationTurnDeleteShimCommand",
    "CopilotGetPanelCompletionsCommand",
    "CopilotGetPromptCommand",
    "CopilotGetVersionCommand",
    "CopilotGitCommitGenerateCommand",
    "CopilotModelsCommand",
    "CopilotNextCompletionCommand",
    "CopilotPreviousCompletionCommand",
    "CopilotRejectCompletionCommand",
    "CopilotSendAnyRequestCommand",
    "CopilotSetModelPolicyCommand",
    "CopilotSignInCommand",
    "CopilotSignInWithGithubTokenCommand",
    "CopilotSignOutCommand",
    "CopilotToggleConversationChatCommand",
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
    CopilotPlugin.cleanup()
    CopilotIgnore.cleanup()
    copilot_ignore_observer.cleanup()
