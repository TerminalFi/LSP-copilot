PACKAGE_NAME = __package__.partition(".")[0]
PACKAGE_VERSION = "0.0.1"

COPILOT_WAITING_COMPLETION_KEY = "copilot.completion.is_waiting"
PHANTOM_KEY = "copilot.completion.previews"

REQ_INITIALIZE = "initialize"
REQ_SET_EDITOR_INFO = "setEditorInfo"
REQ_CHECK_STATUS = "checkStatus"
REQ_SIGN_IN_INITIATE = "signInInitiate"
REQ_SIGN_IN_CONFIRM = "signInConfirm"
REQ_SIGN_OUT = "signOut"
REQ_GET_COMPLETIONS = "getCompletions"
REQ_RECORD_TELEMETRY_CONSENT = "recordTelemetryConsent"
REQ_GET_COMPLETIONS_CYCLING = "getCompletionsCycling"
REQ_NOTIFY_SHOWN = "notifyShown"
REQ_NOTIFY_REJECTED = "notifyRejected"
REQ_NOTIFY_ACCEPTED = "notifyAccepted"

NTFY_STATUS_NOTIFICATION = "statusNotification"
NTFY_LOG_MESSAGE = "LogMessage"
