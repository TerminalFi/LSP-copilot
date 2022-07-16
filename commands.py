from abc import ABCMeta
from functools import partial, wraps

import sublime
from LSP.plugin import Request, Session
from LSP.plugin.core.registry import LspTextCommand
from LSP.plugin.core.typing import Any, Callable, Union, cast

from .constants import (
    PACKAGE_NAME,
    REQ_CHECK_STATUS,
    REQ_NOTIFY_ACCEPTED,
    REQ_NOTIFY_REJECTED,
    REQ_SIGN_IN_CONFIRM,
    REQ_SIGN_IN_INITIATE,
    REQ_SIGN_OUT,
)
from .plugin import CopilotPlugin
from .types import (
    CopilotPayloadNotifyAccepted,
    CopilotPayloadNotifyRejected,
    CopilotPayloadSignInConfirm,
    CopilotPayloadSignInInitiate,
    CopilotPayloadSignOut,
    T_Callable,
)
from .ui import Completion
from .utils import get_setting


def _provide_session(*, failed_return: Any = None) -> Callable[[T_Callable], T_Callable]:
    def decorator(func: T_Callable) -> T_Callable:
        @wraps(func)
        def wrap(self, *arg, **kwargs) -> Any:
            session = self.session_by_name(self.session_name)
            if not session:
                return failed_return
            return func(self, session, *arg, **kwargs)

        return cast(T_Callable, wrap)

    return decorator


class CopilotTextCommand(LspTextCommand, metaclass=ABCMeta):
    session_name = PACKAGE_NAME

    def want_event(self) -> bool:
        return False

    def _record_telemetry(
        self,
        session: Session,
        request: str,
        payload: Union[CopilotPayloadNotifyAccepted, CopilotPayloadNotifyRejected],
    ) -> None:
        if not get_setting(session, "telemetry", False):
            return

        session.send_request(
            Request(request, payload),
            lambda _: None,
        )


class CopilotAcceptSuggestionCommand(CopilotTextCommand):
    @_provide_session()
    def run(self, session: Session, edit: sublime.Edit) -> None:
        completion = Completion(self.view)
        if not completion.is_visible:
            return

        completion.hide()
        self.view.insert(edit, completion.region[1], completion.display_text)

        # TODO: When a suggestion is accept, we need to send a REQ_NOTIFY_REJECTED
        # request with all other completions which weren't accepted
        self._record_telemetry(session, REQ_NOTIFY_ACCEPTED, {"uuid": completion.uuid})


class CopilotRejectSuggestionCommand(CopilotTextCommand):
    @_provide_session()
    def run(self, session: Session, _: sublime.Edit) -> None:
        completion = Completion(self.view)
        completion.hide()

        # TODO: Currently we send the last shown completion UUID, however Copilot can
        # suggest multiple UUID's. We need to return all UUID's which were not accepted
        self._record_telemetry(session, REQ_NOTIFY_REJECTED, {"uuids": [completion.uuid]})


class CopilotCheckStatusCommand(CopilotTextCommand):
    @_provide_session()
    def run(self, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_CHECK_STATUS, {}), self._on_result_check_status)

    def _on_result_check_status(self, payload: Union[CopilotPayloadSignInConfirm, CopilotPayloadSignOut]) -> None:
        if payload.get("status") == "OK":
            CopilotPlugin.set_has_signed_in(True)
            sublime.message_dialog('[LSP-Copilot] Sign in OK with user "{}".'.format(payload.get("user")))
        else:
            CopilotPlugin.set_has_signed_in(False)
            sublime.message_dialog("[LSP-Copilot] You haven't signed in yet.")


class CopilotSignInCommand(CopilotTextCommand):
    @_provide_session()
    def run(self, session: Session, _: sublime.Edit) -> None:
        session.send_request(
            Request(REQ_SIGN_IN_INITIATE, {}),
            partial(self._on_result_sign_in_initiate, session),
        )

    def _on_result_sign_in_initiate(
        self,
        session: Session,
        payload: Union[CopilotPayloadSignInConfirm, CopilotPayloadSignInInitiate],
    ) -> None:
        CopilotPlugin.set_has_signed_in(False)
        if payload.get("status") == "AlreadySignedIn":
            CopilotPlugin.set_has_signed_in(True)
            return
        user_code = payload.get("userCode")
        verification_uri = payload.get("verificationUri")
        if not (user_code and verification_uri):
            return
        sublime.set_clipboard(user_code)
        sublime.run_command("open_url", {"url": verification_uri})
        if not sublime.ok_cancel_dialog(
            "[LSP-Copilot] The device activation code has been copied."
            + " Please paste it in the popup GitHub page. Press OK when completed."
        ):
            return
        session.send_request(
            Request(REQ_SIGN_IN_CONFIRM, {"userCode": user_code}),
            self._on_result_sign_in_confirm,
        )

    def _on_result_sign_in_confirm(self, payload: CopilotPayloadSignInConfirm) -> None:
        if payload.get("status") == "OK":
            CopilotPlugin.set_has_signed_in(True)
            sublime.message_dialog('[LSP-Copilot] Sign in OK with user "{}".'.format(payload.get("user")))

    @_provide_session(failed_return=False)
    def is_enabled(self, session: Session) -> bool:
        return not CopilotPlugin.get_has_signed_in() or get_setting(session, "debug", False)


class CopilotSignOutCommand(CopilotTextCommand):
    @_provide_session()
    def run(self, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_SIGN_OUT, {}), self._on_result_sign_out)

    def _on_result_sign_out(self, payload: CopilotPayloadSignOut) -> None:
        if payload.get("status") == "NotSignedIn":
            CopilotPlugin.set_has_signed_in(False)
            sublime.message_dialog("[LSP-Copilot] Sign out OK. Bye!")
