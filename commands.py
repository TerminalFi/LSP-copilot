from abc import ABCMeta

import sublime
import sublime_plugin
from LSP.plugin import Request
from LSP.plugin.core.registry import LspTextCommand
from LSP.plugin.core.typing import Tuple, Union
from .utils import get_setting

from .constants import PACKAGE_NAME, REQ_CHECK_STATUS, REQ_NOTIFY_ACCEPTED, REQ_SIGN_IN_CONFIRM, REQ_SIGN_IN_INITIATE, REQ_SIGN_OUT
from .plugin import CopilotPlugin
from .types import CopilotPayloadSignInConfirm, CopilotPayloadSignInInitiate, CopilotPayloadSignOut
from .ui import Completion


class CopilotTextCommand(LspTextCommand, metaclass=ABCMeta):
    session_name = PACKAGE_NAME


class CopilotInsertAsIsCommand(CopilotTextCommand):
    def run(self, edit: sublime.Edit, characters: str, region: Tuple[int, int]) -> None:
        self.view.insert(edit, region[1], characters)


class CopilotAcceptSuggestionCommand(CopilotTextCommand):
    def run(self, edit: sublime.Edit) -> None:
        completion = Completion(self.view)

        if not completion.is_visible():
            return

        region = completion.region
        if region is None:
            return

        display_text = completion.display_text
        if display_text is None:
            return

        completion.hide()
        self.view.insert(edit, region[1], display_text)

        session = self.session_by_name(self.session_name)
        if not session:
            return

        def on_notify_accepted(result: str, failed: bool) -> None:
            pass

        session.send_request(
            Request(REQ_NOTIFY_ACCEPTED, {}),
            on_notify_accepted,
        )


class CopilotDismissSuggestionCommand(CopilotTextCommand):
    def run(self, _) -> None:
        completion = Completion(self.view)

        if not completion.is_visible():
            return

        completion.hide()


class CopilotSignInCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        session = self.session_by_name(self.session_name)
        if not session:
            return
        session.send_request(
            Request(REQ_SIGN_IN_INITIATE, {}),
            self._on_result_sign_in_initiate,
        )

    def _on_result_sign_in_initiate(
        self,
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
            "[Copilot] The device activation code has been copied."
            + " Please paste it in the popup GitHub page. Press OK when completed."
        ):
            return
        session = self.session_by_name(self.session_name)
        if not session:
            return
        session.send_request(
            Request(REQ_SIGN_IN_CONFIRM, {"userCode": user_code}),
            self._on_result_sign_in_confirm,
        )

    def _on_result_sign_in_confirm(self, payload: CopilotPayloadSignInConfirm) -> None:
        if payload.get("status") == "OK":
            CopilotPlugin.set_has_signed_in(True)
            sublime.message_dialog('[Copilot] Sign in OK with user "{}".'.format(payload.get("user")))

    def is_enabled(self) -> bool:
        session = self.session_by_name(self.session_name)
        if not session:
            return not CopilotPlugin.get_has_signed_in()
        return (not CopilotPlugin.get_has_signed_in() or get_setting(session, 'debug', False))


class CopilotSignOutCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        session = self.session_by_name(self.session_name)
        if not session:
            return
        session.send_request(
            Request(REQ_SIGN_OUT, {}),
            self._on_result_sign_out,
        )

    def _on_result_sign_out(self, payload: CopilotPayloadSignOut) -> None:
        if payload.get("status") == "NotSignedIn":
            CopilotPlugin.set_has_signed_in(False)
            sublime.message_dialog("[Copilot] Sign out OK. Bye!")

    def is_enabled(self) -> bool:
        session = self.session_by_name(self.session_name)
        if not session:
            return CopilotPlugin.get_has_signed_in()
        return (CopilotPlugin.get_has_signed_in() or get_setting(session, 'debug', False))


class CopilotCheckStatusCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        session = self.session_by_name(self.session_name)
        if not session:
            return
        session.send_request(
            Request(REQ_CHECK_STATUS, {}),
            self._on_result_check_status,
        )

    def _on_result_check_status(self, payload: Union[CopilotPayloadSignInConfirm, CopilotPayloadSignOut]) -> None:
        if payload.get("status") == "OK":
            CopilotPlugin.set_has_signed_in(True)
            sublime.message_dialog('[Copilot] Sign in OK with user "{}".'.format(payload.get("user")))
        else:
            CopilotPlugin.set_has_signed_in(False)
            sublime.message_dialog("[Copilot] You haven't signed in yet.")
