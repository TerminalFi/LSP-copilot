import functools
from abc import ABCMeta
from functools import partial, wraps

import sublime
from LSP.plugin import Request, Session
from LSP.plugin.core.registry import LspTextCommand, LspWindowCommand
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
from .ui import ViewCompletionManager, ViewPanelCompletionManager
from .utils import (
    all_views,
    first,
    get_setting,
    message_dialog,
    ok_cancel_dialog,
    prepare_completion_request,
    status_message,
)

REQUIRE_NOTHING = 0
REQUIRE_SIGN_IN = 1 << 0
REQUIRE_NOT_SIGN_IN = 1 << 1


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


class CopilotCommandBase(metaclass=ABCMeta):
    session_name = PACKAGE_NAME
    requirement = REQUIRE_SIGN_IN

    def _can_meet_requirement(self, session: Session) -> bool:
        if get_setting(session, "debug", False):
            return True

        has_signed_in = CopilotPlugin.get_has_signed_in()
        if ((self.requirement & REQUIRE_SIGN_IN) and not has_signed_in) or (
            (self.requirement & REQUIRE_NOT_SIGN_IN) and has_signed_in
        ):
            return False
        return True


class CopilotTextCommand(CopilotCommandBase, LspTextCommand, metaclass=ABCMeta):
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

    @_provide_session(failed_return=False)
    def is_enabled(self, session: Session) -> bool:
        return self._can_meet_requirement(session)


class CopilotWindowCommand(CopilotCommandBase, LspWindowCommand, metaclass=ABCMeta):
    def is_enabled(self) -> bool:
        session = self.session()
        if not session:
            return False
        return self._can_meet_requirement(session)


class CopilotGetVersionCommand(CopilotTextCommand):
    requirement = REQUIRE_NOTHING

    @_provide_session()
    def run(self, session: Session, _: sublime.Edit) -> None:
        session.send_request(
            Request(REQ_GET_VERSION, {}),
            self._on_result_get_version,
        )

    def _on_result_get_version(self, payload: CopilotPayloadGetVersion) -> None:
        message_dialog("Server version: {}".format(payload["version"]))


class CopilotAskCompletionsCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        plugin = CopilotPlugin.plugin_from_view(self.view)
        if not plugin:
            return

        debounced(
            functools.partial(plugin.request_get_completions, self.view),
            FEATURES_TIMEOUT,
            lambda: not ViewCompletionManager(self.view).is_waiting,
            async_thread=True,
        )


class CopilotAcceptPanelCompletionShimCommand(CopilotWindowCommand):
    def run(self, view_id: int, completion_index: int) -> None:
        view = first(all_views(), lambda view: view.id() == view_id)
        if not view:
            return
        view.run_command("copilot_accept_panel_completion", {"completion_index": completion_index})


class CopilotAcceptPanelCompletionCommand(CopilotTextCommand):
    def run(self, edit: sublime.Edit, completion_index: int) -> None:
        completion_manager = ViewPanelCompletionManager(self.view)
        completion = completion_manager.get_completion(completion_index)
        if not completion:
            return

        # Remove the current line and then insert full text.
        # We don't have to care whether it's an inline completion or not.
        source_line_region = self.view.line(sublime.Region(*completion["region"]))
        self.view.erase(edit, source_line_region)
        self.view.insert(edit, source_line_region.begin(), completion["displayText"])

        completion_manager.close()


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
        source_line_region = self.view.line(completion["point"])
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
        if not params:
            return

        completion_manager = ViewPanelCompletionManager(self.view)
        completion_manager.is_waiting = True
        completion_manager.completions = []

        params["panelId"] = completion_manager.panel_id
        session.send_request(
            Request(REQ_GET_PANEL_COMPLETIONS, params),
            self._on_result_get_panel_completions,
        )

    def _on_result_get_panel_completions(self, payload: CopilotPayloadPanelCompletionSolutionCount) -> None:
        count = payload["solutionCountTarget"]
        status_message("retrieving panel completions: {}".format(count))

        completion_manager = ViewPanelCompletionManager(self.view)
        completion_manager.completion_target_count = count
        completion_manager.open()


class CopilotPreviousCompletionCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        ViewCompletionManager(self.view).show_previous_completion()


class CopilotNextCompletionCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        ViewCompletionManager(self.view).show_next_completion()


class CopilotCheckStatusCommand(CopilotTextCommand):
    requirement = REQUIRE_NOTHING

    @_provide_session()
    def run(self, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_CHECK_STATUS, {}), self._on_result_check_status)

    def _on_result_check_status(self, payload: Union[CopilotPayloadSignInConfirm, CopilotPayloadSignOut]) -> None:
        if payload["status"] == "OK":
            CopilotPlugin.set_has_signed_in(True)
            message_dialog('Sign in OK with user "{}".'.format(payload["user"]))
        else:
            CopilotPlugin.set_has_signed_in(False)
            message_dialog("You haven't signed in yet.")


class CopilotSignInCommand(CopilotTextCommand):
    requirement = REQUIRE_NOT_SIGN_IN

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
        if payload["status"] == "AlreadySignedIn":
            CopilotPlugin.set_has_signed_in(True)
            return
        # TODO: what will happen if the user has no access to Copilot?
        user_code = payload.get("userCode")
        verification_uri = payload.get("verificationUri")
        if not (user_code and verification_uri):
            return
        sublime.set_clipboard(user_code)
        sublime.run_command("open_url", {"url": verification_uri})
        if not ok_cancel_dialog(
            "The device activation code has been copied."
            + " Please paste it in the popup GitHub page. Press OK when completed."
        ):
            return
        session.send_request(
            Request(REQ_SIGN_IN_CONFIRM, {"userCode": user_code}),
            self._on_result_sign_in_confirm,
        )

    def _on_result_sign_in_confirm(self, payload: CopilotPayloadSignInConfirm) -> None:
        if payload["status"] == "OK":
            CopilotPlugin.set_has_signed_in(True)
            message_dialog('Sign in OK with user "{}".'.format(payload["user"]))


class CopilotSignOutCommand(CopilotTextCommand):
    @_provide_session()
    def run(self, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_SIGN_OUT, {}), self._on_result_sign_out)

    def _on_result_sign_out(self, payload: CopilotPayloadSignOut) -> None:
        if payload["status"] == "NotSignedIn":
            CopilotPlugin.set_has_signed_in(False)
            message_dialog("Sign out OK. Bye!")
