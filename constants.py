PACKAGE_NAME = __package__.partition(".")[0]
PACKAGE_VERSION = "0.0.1"

COPILOT_WAITING_COMPLETION_KEY = "copilot.completion.is_waiting"
COPILOT_VIEW_SETTINGS_PREFIX = "copilot.completion"

# ---------------- #
# Copilot requests #
# ---------------- #

REQ_CHECK_STATUS = "checkStatus"  # done
REQ_GET_COMPLETIONS = "getCompletions"  # done
REQ_GET_COMPLETIONS_CYCLING = "getCompletionsCycling"
REQ_NOTIFY_ACCEPTED = "notifyAccepted"  # done
REQ_NOTIFY_REJECTED = "notifyRejected"  # done
REQ_NOTIFY_SHOWN = "notifyShown"
REQ_RECORD_TELEMETRY_CONSENT = "recordTelemetryConsent"
REQ_SET_EDITOR_INFO = "setEditorInfo"  # done
REQ_SIGN_IN_CONFIRM = "signInConfirm"  # done
REQ_SIGN_IN_INITIATE = "signInInitiate"  # done
REQ_SIGN_OUT = "signOut"  # done

# --------------------- #
# Copilot notifications #
# --------------------- #

NTFY_LOG_MESSAGE = "LogMessage"  # done
NTFY_STATUS_NOTIFICATION = "statusNotification"  # done
