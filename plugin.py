from .constants import (
    COPILOT_WAITING_COMPLETION_KEY,
    NTFY_LOG_MESSAGE,
    NTFY_STATUS_NOTIFICATION,
    PACKAGE_NAME,
    PACKAGE_VERSION,
    PHANTOM_KEY,
    REQ_CHECK_STATUS,
    REQ_GET_COMPLETIONS,
    REQ_SET_EDITOR_INFO,
    REQ_SIGN_IN_CONFIRM,
    REQ_SIGN_IN_INITIATE,
    REQ_SIGN_OUT,
)
from .types import (
    CopilotPayloadCompletion,
    CopilotPayloadCompletions,
    CopilotPayloadLogMessage,
    CopilotPayloadSignInConfirm,
    CopilotPayloadSignInInitiate,
    CopilotPayloadSignOut,
    CopilotPayloadStatusNotification,
)
from abc import ABCMeta
from LSP.plugin import Request, filename_to_uri
from LSP.plugin import Session
from LSP.plugin.core.protocol import Request
from LSP.plugin.core.registry import LspTextCommand
from LSP.plugin.core.types import FEATURES_TIMEOUT
from LSP.plugin.core.types import Union, debounced
from LSP.plugin.core.typing import List, Optional, Tuple
from lsp_utils import ApiWrapperInterface
from lsp_utils import notification_handler
from lsp_utils import NpmClientHandler
import functools
import mdpopups
import os
import sublime
import sublime_plugin
import weakref


def plugin_loaded():
    CopilotPlugin.setup()


def plugin_unloaded():
    CopilotPlugin.cleanup()
    CopilotPlugin.plugin_mapping.clear()


def clear_completion_preview(view: sublime.View) -> None:
    mdpopups.erase_phantoms(view=view, key=PHANTOM_KEY)


def get_project_relative_path(file_path: str) -> str:
    folders = sublime.active_window().folders()
    if not folders:
        return file_path
    return min(
        (os.path.relpath(file_path, folder) for folder in folders),
        key=len,
    )


class CopilotPlugin(NpmClientHandler):
    package_name = PACKAGE_NAME
    server_directory = "language-server"
    server_binary_path = os.path.join(server_directory, "copilot", "dist", "agent.js")

    plugin_mapping = weakref.WeakValueDictionary()  # type: weakref.WeakValueDictionary[int, CopilotPlugin]
    _has_signed_in = False

    @classmethod
    def get_has_signed_in(cls) -> bool:
        return cls._has_signed_in

    @classmethod
    def set_has_signed_in(cls, value: bool) -> None:
        cls._has_signed_in = value
        if value:
            sublime.status_message("✈ Copilot has been signed in.")
        else:
            sublime.status_message("⚠ Copilot has NOT been signed in.")

    def __init__(self, session: "weakref.ref[Session]") -> None:
        super().__init__(session)
        sess = session()
        if sess:
            self.plugin_mapping[sess.window.id()] = self

    def on_ready(self, api: ApiWrapperInterface) -> None:
        def on_check_status(result: CopilotPayloadSignInConfirm, _: bool) -> None:
            self.set_has_signed_in(result.get("status") == "OK")

        def on_set_editor_info(result: str, _: bool) -> None:
            pass

        api.send_request(REQ_CHECK_STATUS, {}, on_check_status)
        api.send_request(
            REQ_SET_EDITOR_INFO,
            {
                "editorInfo": {
                    "name": "Sublime Text",
                    "version": sublime.version(),
                },
                "editorPluginInfo": {
                    "name": PACKAGE_NAME,
                    "version": PACKAGE_VERSION,
                },
            },
            on_set_editor_info,
        )

    @classmethod
    def minimum_node_version(cls) -> Tuple[int, int, int]:
        # this should be aligned with VSCode's Nodejs version
        return (16, 0, 0)

    @classmethod
    def plugin_from_view(cls, view: sublime.View) -> Optional["CopilotPlugin"]:
        window = view.window()
        if not window:
            return None
        self = cls.plugin_mapping.get(window.id())
        if not (self and self.is_valid_for_view(view)):
            return None
        return self

    def is_valid_for_view(self, view: sublime.View) -> bool:
        session = self.weaksession()
        return bool(session and session.session_view_for_view_async(view))

    @notification_handler(NTFY_LOG_MESSAGE)
    def _handle_log_message_notification(self, payload: CopilotPayloadLogMessage) -> None:
        pass

    @notification_handler(NTFY_STATUS_NOTIFICATION)
    def _handle_status_notification(self, payload: CopilotPayloadStatusNotification) -> None:
        pass

    def request_get_completions(self, view: sublime.View) -> None:
        clear_completion_preview(view)
        session = self.weaksession()
        syntax = view.syntax()
        sel = view.sel()
        if not (self.get_has_signed_in() and session and syntax and len(sel) == 1):
            return
        setattr(view, COPILOT_WAITING_COMPLETION_KEY, True)
        file_path = view.file_name() or ""
        row, col = view.rowcol(sel[0].begin())
        # this is all hacky
        params = {
            "doc": {
                "source": view.substr(sublime.Region(0, view.size())),
                "tabSize": 4,  # @todo what the hell... I don't get it
                "indentSize": 4,  # @todo what the hell... I don't get it
                "insertSpaces": False,  # @todo what the hell... I don't get it
                "path": file_path,
                "uri": filename_to_uri(file_path),
                "relativePath": get_project_relative_path(file_path),
                "languageId": syntax.scope.rpartition(".")[2],  # @todo there is a mapping in LSP already?
                "position": {"line": row, "character": col},
            }
        }
        session.send_request_async(
            Request(REQ_GET_COMPLETIONS, params),
            functools.partial(self._on_get_completions_async, view),
        )

    def _on_get_completions_async(self, view: sublime.View, payload: CopilotPayloadCompletions) -> None:
        setattr(view, COPILOT_WAITING_COMPLETION_KEY, False)
        completions = payload.get("completions")
        if not completions:
            return
        sublime.set_timeout_async(
            lambda: view.run_command(
                "copilot_preview_completions",
                {"completions": completions},
            )
        )


class EventListener(sublime_plugin.ViewEventListener):
    def on_modified_async(self) -> None:
        plugin = CopilotPlugin.plugin_from_view(self.view)
        if not plugin:
            return
        debounced(
            functools.partial(plugin.request_get_completions, self.view),
            FEATURES_TIMEOUT,
            lambda: not getattr(self.view, COPILOT_WAITING_COMPLETION_KEY, False),
            async_thread=True,
        )


class CopilotTextCommand(LspTextCommand, metaclass=ABCMeta):
    session_name = PACKAGE_NAME


class CopilotPreviewCompletionsCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit, completions: List[CopilotPayloadCompletion], cycle: int = 0) -> None:
        syntax = self.view.syntax()
        if not (syntax and completions):
            return
        cycle = cycle % len(completions)
        syntax_id = syntax.scope.rpartition(".")[2]
        content = '<a href="{}">Accept Suggestion</a>\n```{}\n{}\n```'.format(
            cycle, syntax_id, completions[cycle]["displayText"]
        )
        clear_completion_preview(self.view)
        # This currently doesn't care about where the completion is actually supposed to be
        mdpopups.add_phantom(
            view=self.view,
            key=PHANTOM_KEY,
            region=self.view.sel()[0],
            content=content,
            md=True,
            layout=sublime.LAYOUT_BELOW,
            on_navigate=functools.partial(self._insert_completion, completions=completions),
        )

    def _insert_completion(self, index: str, completions: List[CopilotPayloadCompletion]) -> None:
        idx = int(index)
        if not (0 <= idx < len(completions)):
            return
        completion = completions[idx]
        mdpopups.erase_phantoms(view=self.view, key=PHANTOM_KEY)
        self.view.run_command("insert", {"characters": completion["displayText"]})


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
