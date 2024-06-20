from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum

if sys.version_info < (3, 11):

    class StrEnum(str, Enum):
        __format__ = str.__format__  # type: ignore
        __str__ = str.__str__  # type: ignore
else:
    from enum import StrEnum  # noqa: F401


class NotificationKind(StrEnum):
    """Server notification kinds of the server."""

    # ---- #
    # done #
    # ---- #

    FEATURE_FLAGS_NOTIFICATION = "featureFlagsNotification"
    LOG_MESSAGE = "LogMessage"
    PANEL_SOLUTION = "PanelSolution"
    PANEL_SOLUTION_DONE = "PanelSolutionsDone"
    STATUS_NOTIFICATION = "statusNotification"


class RequestKind(StrEnum):
    """Server request kinds of the server."""

    # ---- #
    # done #
    # ---- #

    CHECK_STATUS = "checkStatus"
    FILE_CHECK_STATUS = "checkFileStatus"
    GET_COMPLETIONS = "getCompletions"
    GET_COMPLETIONS_CYCLING = "getCompletionsCycling"
    GET_PANEL_COMPLETIONS = "getPanelCompletions"
    GET_VERSION = "getVersion"
    NOTIFY_ACCEPTED = "notifyAccepted"
    NOTIFY_REJECTED = "notifyRejected"
    SET_EDITOR_INFO = "setEditorInfo"
    SIGN_IN_CONFIRM = "signInConfirm"
    SIGN_IN_INITIATE = "signInInitiate"
    SIGN_IN_WITH_GITHUB_TOKEN = "signInWithGithubToken"
    SIGN_OUT = "signOut"

    # -------- #
    # not done #
    # -------- #

    NOTIFY_SHOWN = "notifyShown"
    RECORD_TELEMETRY_CONSENT = "recordTelemetryConsent"


@dataclass
class AccountStatus:
    has_signed_in: bool
    is_authorized: bool
