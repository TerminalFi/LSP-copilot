from __future__ import annotations

assert __package__

PACKAGE_NAME = __package__.partition(".")[0]

COPILOT_VIEW_SETTINGS_PREFIX = "copilot.completion"
COPILOT_WINDOW_CONVERSATION_SETTINGS_PREFIX = "copilot.conversation"

# ---------------- #
# Copilot requests #
# ---------------- #

REQ_CHECK_STATUS = "checkStatus"  # done
REQ_FILE_CHECK_STATUS = "checkFileStatus"  # done
REQ_GET_COMPLETIONS = "getCompletions"  # done
REQ_GET_COMPLETIONS_CYCLING = "getCompletionsCycling"  # done
REQ_GET_PANEL_COMPLETIONS = "getPanelCompletions"  # done
REQ_GET_VERSION = "getVersion"  # done
REQ_NOTIFY_ACCEPTED = "notifyAccepted"  # done
REQ_NOTIFY_REJECTED = "notifyRejected"  # done
REQ_NOTIFY_SHOWN = "notifyShown"
REQ_RECORD_TELEMETRY_CONSENT = "recordTelemetryConsent"
REQ_SET_EDITOR_INFO = "setEditorInfo"  # done
REQ_SIGN_IN_CONFIRM = "signInConfirm"  # done
REQ_SIGN_IN_INITIATE = "signInInitiate"  # done
REQ_SIGN_IN_WITH_GITHUB_TOKEN = "signInWithGithubToken"  # done
REQ_SIGN_OUT = "signOut"  # done

# --------------------- #
# Copilot Chat requests #
# --------------------- #

REQ_CONVERSATION_AGENTS = "conversation/agents"
REQ_CONVERSATION_CONTEXT = "conversation/context"
REQ_CONVERSATION_COPY_CODE = "conversation/copyCode"
REQ_CONVERSATION_CREATE = "conversation/create"
REQ_CONVERSATION_DESTROY = "conversation/destroy"
REQ_CONVERSATION_INSERT_CODE = "conversation/insertCode"
REQ_CONVERSATION_PERSISTANCE = "conversation/persistance"
REQ_CONVERSATION_PRECONDITIONS = "conversation/preconditions"
REQ_CONVERSATION_RATING = "conversation/rating"
REQ_CONVERSATION_TEMPLATES = "conversation/templates"
REQ_CONVERSATION_TURN = "conversation/turn"
REQ_CONVERSATION_TURN_DELETE = "conversation/turnDelete"

# --------------------- #
# Copilot notifications #
# --------------------- #

NTFY_FEATURE_FLAGS_NOTIFICATION = "featureFlagsNotification"  # done
NTFY_LOG_MESSAGE = "LogMessage"  # done
NTFY_PANEL_SOLUTION = "PanelSolution"  # done
NTFY_PANEL_SOLUTION_DONE = "PanelSolutionsDone"  # done
NTFY_PROGRESS = "$/progress"
NTFY_STATUS_NOTIFICATION = "statusNotification"  # done
