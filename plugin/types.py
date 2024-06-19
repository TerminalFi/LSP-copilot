from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Literal, Tuple, TypedDict, TypeVar

T_Callable = TypeVar("T_Callable", bound=Callable[..., Any])


@dataclass
class AccountStatus:
    has_signed_in: bool
    is_authorized: bool


# ---------------------------- #
# realted to Sublime Text APIs #
# ---------------------------- #

StPoint = int
StRegion = Tuple[StPoint, StPoint]


class StLayout(TypedDict, total=True):
    cols: list[float]
    rows: list[float]
    cells: list[list[int]]


class NetworkProxy(TypedDict, total=True):
    host: str
    port: int
    username: str
    password: str
    rejectUnauthorized: bool


# --------------- #
# Copilot payload #
# --------------- #


class CopilotPayloadFileStatus(TypedDict, total=True):
    status: Literal["not included", "included"]


class CopilotPayloadCompletionPosition(TypedDict, total=True):
    character: int
    line: int


class CopilotPayloadCompletionRange(TypedDict, total=True):
    start: CopilotPayloadCompletionPosition
    end: CopilotPayloadCompletionPosition


class CopilotPayloadCompletion(TypedDict, total=True):
    text: str
    position: CopilotPayloadCompletionPosition
    uuid: str
    range: CopilotPayloadCompletionRange
    displayText: str
    point: StPoint
    region: StRegion


class CopilotPayloadCompletions(TypedDict, total=True):
    completions: list[CopilotPayloadCompletion]


class CopilotPayloadFeatureFlagsNotification(TypedDict, total=True):
    ssc: bool
    chat: bool
    rt: bool


class CopilotPayloadGetVersion(TypedDict, total=True):
    version: str
    """E.g., `"1.202.0"`."""
    buildType: str
    """E.g., `"prod"`."""
    runtimeVersion: str
    """E.g., `"node/20.14.0"`."""


class CopilotPayloadNotifyAccepted(TypedDict, total=True):
    uuid: str


class CopilotPayloadNotifyRejected(TypedDict, total=True):
    uuids: list[str]


class CopilotPayloadSignInInitiate(TypedDict, total=True):
    verificationUri: str
    status: str
    userCode: str
    expiresIn: int
    interval: int


class CopilotPayloadSignInWithGithubToken(TypedDict, total=True):
    user: str
    githubToken: str


class CopilotPayloadSignInConfirm(TypedDict, total=True):
    status: Literal["AlreadySignedIn", "MaybeOk", "NotAuthorized", "NotSignedIn", "OK"]
    user: str


class CopilotPayloadSignOut(TypedDict, total=True):
    status: Literal["NotSignedIn"]


class CopilotPayloadLogMessage(TypedDict, total=True):
    metadataStr: str
    extra: str
    level: int
    message: str


class CopilotPayloadStatusNotification(TypedDict, total=True):
    message: str
    status: Literal["InProgress", "Normal"]


class CopilotPayloadPanelSolution(TypedDict, total=True):
    displayText: str
    solutionId: str
    score: int
    panelId: str
    completionText: str
    range: CopilotPayloadCompletionRange
    region: StRegion


class CopilotPayloadPanelCompletionSolutionCount(TypedDict, total=True):
    solutionCountTarget: int
