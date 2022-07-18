import functools
from abc import ABCMeta
from functools import partial, wraps

import sublime
from LSP.plugin import Request, Session
from LSP.plugin.core.registry import LspTextCommand
from LSP.plugin.core.types import FEATURES_TIMEOUT, debounced
from LSP.plugin.core.typing import Any, Callable, Union, cast

from .constants import (
    PACKAGE_NAME,
    REQ_CHECK_STATUS,
    REQ_GET_PANEL_COMPLETIONS,
    REQ_GET_VERSION,
    REQ_NOTIFY_ACCEPTED,
    REQ_NOTIFY_REJECTED,
    REQ_SIGN_IN_CONFIRM,
    REQ_SIGN_IN_INITIATE,
    REQ_SIGN_OUT,
)
from .plugin import CopilotPlugin
from .types import (
    CopilotPayloadGetVersion,
    CopilotPayloadNotifyAccepted,
    CopilotPayloadNotifyRejected,
    CopilotPayloadPanelCompletionSolutionCount,
    CopilotPayloadSignInConfirm,
    CopilotPayloadSignInInitiate,
    CopilotPayloadSignOut,
    T_Callable,
)
from .ui import ViewCompletionManager
from .utils import (
    erase_copilot_view_setting,
    get_copilot_view_setting,
    get_setting,
    prepare_completion_request,
    set_copilot_view_setting,
)


def _provide_session(*, failed_return: Any = None) -> Callable[[T_Callable], T_Callable]:
    def decorator(func: T_Callable) -> T_Callable:
        @wraps(func)
        def wrap(self, *arg, **kwargs) -> Any:
            """
            The first argument is always `self` for a decorated method.
            We want to provide `session` right after it. If we failed to find a `session`,
            then it will be early failed and return `failed_return`.
            """
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


class CopilotGetVersionCommand(CopilotTextCommand):
    @_provide_session()
    def run(self, session: Session, _: sublime.Edit) -> None:
        session.send_request(
            Request(REQ_GET_VERSION, {}),
            self._on_result_get_version,
        )

    def _on_result_get_version(self, payload: CopilotPayloadGetVersion) -> None:
        sublime.message_dialog("[LSP-copilot] Server version: {}".format(payload.get("version", "unknown")))


class CopilotAskCompletionsCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        plugin = CopilotPlugin.plugin_from_view(self.view)
        if not plugin:
            return

        debounced(
            functools.partial(plugin.request_get_completions, self.view),
            FEATURES_TIMEOUT,
            lambda: not get_copilot_view_setting(self.view, "is_waiting_completions", False),
            async_thread=True,
        )


class CopilotAcceptCompletionCommand(CopilotTextCommand):
    @_provide_session()
    def run(self, session: Session, edit: sublime.Edit) -> None:
        completion_manager = ViewCompletionManager(self.view)
        if not completion_manager.is_visible:
            return

        completion_manager.hide()

        completion = completion_manager.current_completion
        if not completion:
            return

        # Remove the current line and then insert full text.
        # We don't have to care whether it's an inline completion or not.
        source_line_region = self.view.line(completion["positionSt"])
        self.view.erase(edit, source_line_region)
        self.view.insert(edit, source_line_region.begin(), completion["text"])

        # notify the current completion as accepted
        self._record_telemetry(session, REQ_NOTIFY_ACCEPTED, {"uuid": completion["uuid"]})

        # notify all other completions as rejected
        other_uuids = [completion["uuid"] for completion in completion_manager.completions]
        other_uuids.remove(completion["uuid"])
        if other_uuids:
            self._record_telemetry(session, REQ_NOTIFY_REJECTED, {"uuids": other_uuids})


class CopilotRejectCompletionCommand(CopilotTextCommand):
    @_provide_session()
    def run(self, session: Session, _: sublime.Edit) -> None:
        completion_manager = ViewCompletionManager(self.view)
        completion_manager.hide()

        # notify all completions as rejected
        self._record_telemetry(
            session,
            REQ_NOTIFY_REJECTED,
            {"uuids": [completion["uuid"] for completion in completion_manager.completions]},
        )


class CopilotGetPanelCompletionsCommand(CopilotTextCommand):
    @_provide_session()
    def run(self, session: Session, _: sublime.Edit) -> None:
        params = prepare_completion_request(view=self.view)
        if params is None:
            return

        copilot_panel_id = "copilot://{}".format(self.view.id())
        params["panelId"] = copilot_panel_id

        set_copilot_view_setting(self.view, "panel_id", copilot_panel_id)
        set_copilot_view_setting(self.view, "is_waiting_panel_completions", True)
        erase_copilot_view_setting(self.view, "panel_completions")

        session.send_request(
            Request(REQ_GET_PANEL_COMPLETIONS, params),
            self._on_result_get_panel_completions,
        )

    def _on_result_get_panel_completions(self, payload: CopilotPayloadPanelCompletionSolutionCount) -> None:
        count = payload.get("solutionCountTarget", 0)
        sublime.status_message("[LSP-copilot] Retrieving Panel Completions: {}".format(count))
        set_copilot_view_setting(self.view, "panel_completion_target_count", count)


class CopilotPreviousCompletionCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        ViewCompletionManager(self.view).show_previous_completion()


class CopilotNextCompletionCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        ViewCompletionManager(self.view).show_next_completion()


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
