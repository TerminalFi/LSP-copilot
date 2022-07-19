import functools
import os
import weakref

import sublime
from LSP.plugin import Request, Session
from LSP.plugin.core.typing import Optional, Tuple
from lsp_utils import ApiWrapperInterface, NpmClientHandler, notification_handler

from .constants import (
    NTFY_LOG_MESSAGE,
    NTFY_PANEL_SOLUTION,
    NTFY_PANEL_SOLUTION_DONE,
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
    CopilotPayloadPanelSolution,
    CopilotPayloadSignInConfirm,
    CopilotPayloadStatusNotification,
)
from .ui import ViewCompletionManager, ViewPanelCompletionManager
from .utils import (
    all_st_views,
    first,
    prepare_completion_request,
    preprocess_completions,
    preprocess_panel_completions,
    remove_prefix,
)


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
                cm = ViewCompletionManager(view)
                cm.is_visible = False
                cm.is_waiting = False

                pcm = ViewPanelCompletionManager(view)
                pcm.is_waiting = False

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

    @notification_handler(NTFY_PANEL_SOLUTION)
    def _handle_panel_solution_notification(self, payload: CopilotPayloadPanelSolution) -> None:
        view_id = int(remove_prefix(payload.get("panelId"), "copilot://"))
        target_view = first(all_st_views(), lambda view: view.id() == view_id)
        if not target_view:
            return

        preprocess_panel_completions(target_view, [payload])

        completion_manager = ViewPanelCompletionManager(target_view)
        completions = completion_manager.completions
        completions.append(payload)
        completion_manager.completions = completions
        completion_manager.update()

    @notification_handler(NTFY_PANEL_SOLUTION_DONE)
    def _handle_panel_solution_done_notification(self, payload) -> None:
        view_id = int(remove_prefix(payload.get("panelId"), "copilot://"))
        target_view = first(all_st_views(), lambda view: view.id() == view_id)
        if not target_view:
            return

        ViewPanelCompletionManager(target_view).is_waiting = False

    @notification_handler(NTFY_STATUS_NOTIFICATION)
    def _handle_status_notification_notification(self, payload: CopilotPayloadStatusNotification) -> None:
        pass

    def request_get_completions(self, view: sublime.View) -> None:
        completion_manager = ViewCompletionManager(view)
        completion_manager.hide()

        session = self.weaksession()
        sel = view.sel()
        if not (self.get_has_signed_in() and session and len(sel) == 1):
            return

        params = prepare_completion_request(view)
        if not params:
            return

        completion_manager.is_waiting = True
        session.send_request_async(
            Request(REQ_GET_COMPLETIONS, params),
            functools.partial(self._on_get_completions, view, region=sel[0].to_tuple()),
        )

    def _on_get_completions(
        self,
        view: sublime.View,
        payload: CopilotPayloadCompletions,
        region: Tuple[int, int],
    ) -> None:
        completion_manager = ViewCompletionManager(view)
        completion_manager.is_waiting = False

        # re-request completions because the cursor position changed during awaiting Copilot's response
        if view.sel()[0].to_tuple() != region:
            self.request_get_completions(view)
            return

        completions = payload.get("completions")
        if not completions:
            return

        preprocess_completions(view, completions)
        completion_manager.show(completions, 0)
