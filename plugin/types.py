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


# --------------------- #
#  Copilot Chat Types   #
# --------------------- #


# class CopilotRequestCoversationPreconditions(TypedDict, total=True):
#     pass


# class CopilotRequestCoversationPersistance(TypedDict, total=True):
#     pass


# class CopilotRequestCoversationChatCreate(TypedDict, total=True):
#     pass


# class CopilotRequestCoversationChatTurn(TypedDict, total=True):
#     workDoneToken: str | int
#     conversationId: str
#     message: str
#     followUp: dict[str, str]
#     options: dict[str, str]  # {}
#     doc: dict[str, str]
#     computeSuggestions: bool
#     references: list[dict[str, str]]  # List of doc type
#     workspaceFolder: str

#     # doc = {
#     #             uri: Qi.Type.String(),
#     #             position: Qi.Type.Optional(
#     #                 Qi.Type.Object({
#     #                     line: Qi.Type.Number({ minimum: 0 }),
#     #                     character: Qi.Type.Number({ minimum: 0 }),
#     #                 }),
#     #             ),
#     #             visibleRange: Qi.Type.Optional(R8),
#     #             selection: Qi.Type.Optional(R8),
#     #             openedAt: Qi.Type.Optional(Qi.Type.String()),
#     #             activeAt: Qi.Type.Optional(Qi.Type.String()),
#     #         }
#     # {
#     #         workDoneToken: no.Type.Union([no.Type.String(), no.Type.Number()]),
#     #         conversationId: no.Type.String(),
#     #         message: no.Type.String(),
#     #         followUp: no.Type.Optional(
#     #             no.Type.Object({ id: no.Type.String(), type: no.Type.String() }),
#     #         ),
#     #         options: no.Type.Optional(Mn),
#     #         doc: no.Type.Optional(Z0),
#     #         computeSuggestions: no.Type.Optional(no.Type.Boolean()),
#     #         references: no.Type.Optional(no.Type.Array(k8)),
#     #         workspaceFolder: no.Type.Optional(no.Type.String()),
#     #     }


class CopilotRequestCoversationAgent(TypedDict, total=True):
    id: str
    description: str
