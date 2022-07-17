import functools
import os
import weakref

import sublime
from LSP.plugin import Request, Session, filename_to_uri
from LSP.plugin.core.typing import Optional, Tuple
from lsp_utils import ApiWrapperInterface, NpmClientHandler, notification_handler

from .constants import (
    NTFY_LOG_MESSAGE,
    NTFY_STATUS_NOTIFICATION,
    PACKAGE_NAME,
    PACKAGE_VERSION,
    REQ_CHECK_STATUS,
    REQ_GET_COMPLETIONS,
    REQ_SET_EDITOR_INFO,
)
from .types import (
    CopilotPayloadCompletions,
    CopilotPayloadLogMessage,
    CopilotPayloadSignInConfirm,
    CopilotPayloadStatusNotification,
)
from .ui import ViewCompletionManager
from .utils import get_project_relative_path, preprocess_completions, set_copilot_view_setting


def plugin_loaded() -> None:
    CopilotPlugin.setup()


def plugin_unloaded() -> None:
    CopilotPlugin.cleanup()
    CopilotPlugin.plugin_mapping.clear()


class CopilotPlugin(NpmClientHandler):
    package_name = PACKAGE_NAME
    server_directory = "language-server"
    server_binary_path = os.path.join(
        server_directory,
        "node_modules",
        "copilot-node-server",
        "copilot",
        "dist",
        "agent.js",
    )

    plugin_mapping = weakref.WeakValueDictionary()  # type: weakref.WeakValueDictionary[int, CopilotPlugin]
    _has_signed_in = False

    def __init__(self, session: "weakref.ref[Session]") -> None:
        super().__init__(session)
        sess = session()
        if sess:
            self.plugin_mapping[sess.window.id()] = self

        # ST persists view setting after getting closed so we have to reset some status
        for window in sublime.windows():
            for view in window.views(include_transient=True):
                set_copilot_view_setting(view, "is_visible", False)
                set_copilot_view_setting(view, "is_waiting", False)

    def on_ready(self, api: ApiWrapperInterface) -> None:
        def on_check_status(result: CopilotPayloadSignInConfirm, failed: bool) -> None:
            self.set_has_signed_in(result.get("status") == "OK")

        def on_set_editor_info(result: str, failed: bool) -> None:
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
    def get_has_signed_in(cls) -> bool:
        return cls._has_signed_in

    @classmethod
    def set_has_signed_in(cls, value: bool) -> None:
        cls._has_signed_in = value
        if value:
            msg = "✈ Copilot has been signed in."
        else:
            msg = "⚠ Copilot has NOT been signed in."
        print("[{}] {}".format(PACKAGE_NAME, msg))
        sublime.status_message(msg)

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
        ViewCompletionManager(view).hide()

        session = self.weaksession()
        syntax = view.syntax()
        sel = view.sel()
        if not (self.get_has_signed_in() and session and syntax and len(sel) == 1):
            return

        cursor = sel[0]
        file_path = view.file_name() or ""
        row, col = view.rowcol(cursor.begin())
        params = {
            "doc": {
                "source": view.substr(sublime.Region(0, view.size())),
                "tabSize": view.settings().get("tab_size", 4),
                "indentSize": 1,  # there is no such concept in ST
                "insertSpaces": view.settings().get("translate_tabs_to_spaces", False),
                "path": file_path,
                "uri": file_path and filename_to_uri(file_path),
                "relativePath": get_project_relative_path(file_path),
                "languageId": syntax.scope.rpartition(".")[2],  # @todo there is a mapping in LSP already?
                "position": {"line": row, "character": col},
            }
        }

        set_copilot_view_setting(view, "is_waiting", True)
        session.send_request_async(
            Request(REQ_GET_COMPLETIONS, params),
            functools.partial(self._on_get_completions, view, region=cursor.to_tuple()),
        )

    def _on_get_completions(
        self,
        view: sublime.View,
        payload: CopilotPayloadCompletions,
        region: Tuple[int, int],
    ) -> None:
        set_copilot_view_setting(view, "is_waiting", False)

        # re-request completions because the cursor position changed during awaiting Copilot's response
        if view.sel()[0].to_tuple() != region:
            self.request_get_completions(view)
            return

        completions = payload.get("completions")
        if not completions:
            return

        preprocess_completions(view, completions)

        ViewCompletionManager(view).show(completions, 0)
