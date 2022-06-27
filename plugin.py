from LSP.plugin import Request, Session
from LSP.plugin.core.registry import LspTextCommand
from LSP.plugin.core.typing import Any, Dict, Optional, Tuple
from lsp_utils import ApiWrapperInterface, NpmClientHandler
from lsp_utils import notification_handler
from lsp_utils import request_handler
from abc import ABCMeta
import os
import sublime

SESSION_NAME = "LSP-copilot"


def plugin_loaded():
    LspCopilotPlugin.setup()


def plugin_unloaded():
    LspCopilotPlugin.cleanup()


class LspCopilotPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = "language-server"
    server_binary_path = os.path.join(
        server_directory,
        "copilot",
        "dist",
        "agent.js",
    )

    has_signed_in = False

    def on_ready(self, api: ApiWrapperInterface) -> None:
        def do_copilot_sign_in(payload: Any, failed: bool) -> None:
            view = sublime.active_window().active_view()
            if view:
                view.run_command("lsp_copilot_sign_in")

        api.send_request(
            "setEditorInfo",
            {
                "editorInfo": {"name": "Sublime Text", "version": sublime.version()},
                "editorPluginInfo": {"name": self.package_name, "version": "0.0.1"},
            },
            do_copilot_sign_in,
        )

    @classmethod
    def minimum_node_version(cls) -> Tuple[int, int, int]:
        # this should be aligned with VSCode's Nodejs version
        return (16, 0, 0)


class LspCopilotCommand(LspTextCommand, metaclass=ABCMeta):
    session_name = SESSION_NAME

    def get_session_if_signed_in(self) -> Optional[Session]:
        session = self.session_by_name(self.session_name)
        if session and LspCopilotPlugin.has_signed_in:
            return session


class LspCopilotSignInCommand(LspCopilotCommand):
    def run(self, _: sublime.Edit):
        session = self.session_by_name(self.session_name)
        if session is None:
            return
        session.send_request(Request("signInInitiate", {}), self._on_result_sign_in_initiate)

    def _on_result_sign_in_initiate(self, payload: Dict[str, Any]) -> None:
        # {'verificationUri': 'https://github.com/login/device', 'status': 'PromptUserDeviceFlow', 'userCode': '57B4-6102', 'expiresIn': 899, 'interval': 5}
        if payload.get("status") == "AlreadySignedIn":
            LspCopilotPlugin.has_signed_in = True
            return
        user_code = payload.get("userCode")
        verification_uri = payload.get("verificationUri")
        if user_code and verification_uri:
            sublime.set_clipboard(user_code)
            sublime.run_command("open_url", {"url": verification_uri})
            if not sublime.ok_cancel_dialog(
                "[LSP-copilot] The device activation code has been copied."
                + " Please paste it in the popup website. Press OK when completed."
            ):
                LspCopilotPlugin.has_signed_in = False
                return
            session = self.session_by_name(self.session_name)
            if session is None:
                return
            session.send_request(Request("signInConfirm", {"userCode": user_code}), self._on_result_sign_in_confirm)

    def _on_result_sign_in_confirm(self, payload: Dict[str, Any]) -> None:
        if payload.get("status") == "OK":
            LspCopilotPlugin.has_signed_in = True
            sublime.message_dialog('[LSP-copilot] Sign in OK with user "{}".'.format(payload.get("user")))
