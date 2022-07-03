from LSP.plugin.core.types import TypedDict
from LSP.plugin.core.typing import List, Literal

CopilotPayloadCompletionPosition = TypedDict(
    "CopilotPayloadCompletionPosition",
    {
        "character": int,
        "line": int,
    },
    total=True,
)

CopilotPayloadCompletionRange = TypedDict(
    "CopilotPayloadCompletionRange",
    {
        "begin": CopilotPayloadCompletionPosition,
        "end": CopilotPayloadCompletionPosition,
    },
    total=True,
)

CopilotPayloadCompletion = TypedDict(
    "CopilotPayloadCompletion",
    {
        "text": str,
        "position": CopilotPayloadCompletionPosition,
        "uuid": str,
        "range": CopilotPayloadCompletionRange,
        "displayText": str,
    },
    total=True,
)

CopilotPayloadCompletions = TypedDict(
    "CopilotPayloadCompletions",
    {
        "completions": List[CopilotPayloadCompletion],
    },
    total=True,
)

CopilotPayloadSignInInitiate = TypedDict(
    "CopilotPayloadSignInInitiate",
    {
        "verificationUri": str,
        "status": str,
        "userCode": str,
        "expiresIn": int,
        "interval": int,
    },
    total=True,
)

CopilotPayloadSignInConfirm = TypedDict(
    "CopilotPayloadSignInConfirm",
    {
        "status": Literal["AlreadySignedIn", "NotSignedIn", "OK"],
        "user": str,
    },
    total=True,
)

CopilotPayloadSignOut = TypedDict(
    "CopilotPayloadSignOut",
    {
        "status": Literal["NotSignedIn"],
    },
    total=True,
)

CopilotPayloadLogMessage = TypedDict(
    "CopilotPayloadLogMessage",
    {
        "metadataStr": str,
        "extra": str,
        "level": int,
        "message": str,
    },
    total=True,
)

CopilotPayloadStatusNotification = TypedDict(
    "CopiloPayloadStatusNotification",
    {
        "message": str,
        "status": Literal["InProgress", "Normal"],
    },
    total=True,
)
