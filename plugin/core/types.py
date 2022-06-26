import socket
from typing import Dict, List, Optional

TCP_CONNECT_TIMEOUT = 5  # seconds

INITIALIZE = 'initialize'
SET_EDITOR_INFO = 'setEditorInfo'
CHECK_STATUS = 'checkStatus'
SIGN_IN_INITIATE = 'signInInitiate'
SIGN_IN_CONFIRM = 'signInConfirm'
SIGN_OUT = 'signOut'
GET_COMPLETIONS = 'getCompletions'
RECORD_TELEMETRY_CONSENT = 'recordTelemetryConsent'
GET_COMPLETIONS_CYCLING = 'getCompletionsCycling'
NOTIFY_SHOWN = 'notifyShown'
NOTIFY_REJECTED = 'notifyRejected'
NOTIFY_ACCEPTED = 'notifyAccepted'

STATUS_NOTIFICATION = 'statusNotification'
LOG_MESSAGE = 'LogMessage'

class TransportConfig:
    __slots__ = ("name", "command", "env", "listener_socket")

    def __init__(
        self,
        name: str,
        command: List[str],
        env: Dict[str, str],
        listener_socket: Optional[socket.socket]
    ) -> None:
        if not command:
            raise ValueError(' "command" not is provided; cannot start a language server')
        self.name = name
        self.command = command
        self.env = env
        self.listener_socket = listener_socket


class Document:
    def __init__(self) -> None:
        pass

class Completion:
    def __init__(self) -> None:
        pass

class Completions:
    def __init__(self) -> None:
        pass
