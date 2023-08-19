import functools
import json
import os
import weakref
from functools import wraps
from urllib.parse import urlparse

import sublime
from LSP.plugin import Request, Session
from LSP.plugin.core.collections import DottedDict
from LSP.plugin.core.typing import Any, Callable, Dict, Optional, Tuple, Union, cast
from lsp_utils import ApiWrapperInterface, NpmClientHandler, notification_handler

from .constants import (
    NTFY_FEATURE_FLAGS_NOTIFICATION,
    NTFY_LOG_MESSAGE,
    NTFY_PANEL_SOLUTION,
    NTFY_PANEL_SOLUTION_DONE,
    NTFY_STATUS_NOTIFICATION,
    PACKAGE_NAME,
    REQ_CHECK_STATUS,
    REQ_GET_COMPLETIONS,
    REQ_GET_COMPLETIONS_CYCLING,
    REQ_SET_EDITOR_INFO,
)
from .types import (
    AccountStatus,
    CopilotPayloadCompletions,
    CopilotPayloadFeatureFlagsNotification,
    CopilotPayloadLogMessage,
    CopilotPayloadPanelSolution,
    CopilotPayloadSignInConfirm,
    CopilotPayloadStatusNotification,
    NetworkProxy,
    T_Callable,
)
from .ui import ViewCompletionManager, ViewPanelCompletionManager
from .utils import (
    all_views,
    debounce,
    get_session_setting,
    prepare_completion_request,
    preprocess_completions,
    preprocess_panel_completions,
    status_message,
)


def plugin_loaded() -> None:
    CopilotPlugin.setup()


def plugin_unloaded() -> None:
    CopilotPlugin.cleanup()


def _guard_view(*, failed_return: Any = None) -> Callable[[T_Callable], T_Callable]:
    """
    The first two arguments have to be `self` and `view` for a decorated method.
    If `view` doesn't meeting some requirements, it will be early failed and return `failed_return`.
    """

    def decorator(func: T_Callable) -> T_Callable:
        @wraps(func)
        def wrapped(self: Any, view: sublime.View, *arg, **kwargs) -> Any:
            view_settings = view.settings()
            if not (
                view.is_valid()
                and not view.element()
                and not view.is_read_only()
                and not view_settings.get("command_mode")
                and not view_settings.get("is_widget")
            ):
                return failed_return

            return func(self, view, *arg, **kwargs)

        return cast(T_Callable, wrapped)

    return decorator


class CopilotPlugin(NpmClientHandler):
    package_name = PACKAGE_NAME
    server_directory = "language-server"
    server_binary_path = os.path.join(
        server_directory,
        "node_modules",
        "copilot-node-server",
        "bin",
        "copilot-node-server",
    )

    plugin_mapping = weakref.WeakValueDictionary()  # type: weakref.WeakValueDictionary[int, CopilotPlugin]

    # account status
    _has_signed_in = False
    _is_authorized = False

    def __init__(self, session: "weakref.ref[Session]") -> None:
        super().__init__(session)
        sess = session()
        if sess:
            self.plugin_mapping[sess.window.id()] = self

        # Note that ST persists view settings after ST is closed. If the user closes ST
        # during awaiting Copilot's response, the internal state management will be corrupted.
        # So, we have to reset some status when started.
        for view in all_views():
            ViewCompletionManager(view).reset()
            ViewPanelCompletionManager(view).reset()

    def on_ready(self, api: ApiWrapperInterface) -> None:
        def on_check_status(result: CopilotPayloadSignInConfirm, failed: bool) -> None:
            self.set_account_status(
                signed_in=result["status"] in {"NotAuthorized", "OK"},
                authorized=result["status"] == "OK",
            )

        def on_set_editor_info(result: str, failed: bool) -> None:
            pass

        api.send_request(REQ_CHECK_STATUS, {}, on_check_status)
        api.send_request(REQ_SET_EDITOR_INFO, self.editor_info(), on_set_editor_info)

    def on_settings_changed(self, settings: DottedDict) -> None:
        def parse_proxy(proxy: str) -> Optional[NetworkProxy]:
            # in the form of "username:password@host:port" or "host:port"
            if not proxy:
                return None
            parsed = urlparse("http://" + proxy)
            return {
                "host": parsed.hostname or "",
                "port": parsed.port or 80,
                "username": parsed.username or "",
                "password": parsed.password or "",
                "rejectUnauthorized": True,
            }

        session = self.weaksession()
        if not session:
            return

        editor_info = self.editor_info()

        networkProxy = parse_proxy(settings.get("proxy") or "")
        if networkProxy:
            editor_info["networkProxy"] = networkProxy

        session.send_request(Request(REQ_SET_EDITOR_INFO, editor_info), lambda response: None)

    @staticmethod
    def version() -> str:
        """Return this plugin's version. If it's not installed by Package Control, return `"unknown"`."""
        try:
            return json.loads(sublime.load_resource("Packages/{}/package-metadata.json".format(PACKAGE_NAME)))[
                "version"
            ]
        except Exception:
            return "unknown"

    @classmethod
    def editor_info(cls) -> Dict[str, Any]:
        return {
            "editorInfo": {
                "name": "Sublime Text",
                "version": sublime.version(),
            },
            "editorPluginInfo": {
                "name": PACKAGE_NAME,
                "version": cls.version(),
            },
        }

    @classmethod
    def required_node_version(cls) -> str:
        """
        Testing playground at https://semver.npmjs.com
        And `0.0.0` means "no restrictions".
        """
        return ">=16"

    @classmethod
    def get_account_status(cls) -> AccountStatus:
        """Return `(has_signed_in, is_authorized)`."""
        return AccountStatus(cls._has_signed_in, cls._is_authorized)

    @classmethod
    def set_account_status(
        cls,
        *,
        signed_in: Optional[bool] = None,
        authorized: Optional[bool] = None,
        quiet: bool = False
        # format delimiter
    ) -> None:
        if signed_in is not None:
            cls._has_signed_in = signed_in
        if authorized is not None:
            cls._is_authorized = authorized

        if not quiet:
            if not cls._has_signed_in:
                icon, msg = "❌", "has NOT been signed in."
            elif not cls._is_authorized:
                icon, msg = "⚠", "has signed in but not authorized."
            else:
                icon, msg = "✈", "has been signed in and authorized."
            status_message(msg, icon_=icon, console_=True)

    @classmethod
    def from_view(cls, view: sublime.View) -> Optional["CopilotPlugin"]:
        window = view.window()
        if not window:
            return None
        self = cls.plugin_mapping.get(window.id())
        if not (self and self.is_valid_for_view(view)):
            return None
        return self

    @classmethod
    def plugin_session(cls, view: sublime.View) -> Union[Tuple[None, None], Tuple["CopilotPlugin", Optional[Session]]]:
        plugin = cls.from_view(view)
        return (plugin, plugin.weaksession()) if plugin else (None, None)

    def is_valid_for_view(self, view: sublime.View) -> bool:
        session = self.weaksession()
        return bool(session and session.session_view_for_view_async(view))

    @notification_handler(NTFY_FEATURE_FLAGS_NOTIFICATION)
    def _handle_feature_flags_notification(self, payload: CopilotPayloadFeatureFlagsNotification) -> None:
        pass

    @notification_handler(NTFY_LOG_MESSAGE)
    def _handle_log_message_notification(self, payload: CopilotPayloadLogMessage) -> None:
        pass

    @notification_handler(NTFY_PANEL_SOLUTION)
    def _handle_panel_solution_notification(self, payload: CopilotPayloadPanelSolution) -> None:
        view = ViewPanelCompletionManager.find_view_by_panel_id(payload["panelId"])
        if not view:
            return

        preprocess_panel_completions(view, [payload])

        completion_manager = ViewPanelCompletionManager(view)
        completion_manager.append_completion(payload)
        completion_manager.update()

    @notification_handler(NTFY_PANEL_SOLUTION_DONE)
    def _handle_panel_solution_done_notification(self, payload) -> None:
        view = ViewPanelCompletionManager.find_view_by_panel_id(payload["panelId"])
        if not view:
            return

        completion_manager = ViewPanelCompletionManager(view)
        completion_manager.is_waiting = False
        completion_manager.update()

    @notification_handler(NTFY_STATUS_NOTIFICATION)
    def _handle_status_notification_notification(self, payload: CopilotPayloadStatusNotification) -> None:
        pass

    @_guard_view()
    @debounce()
    def request_get_completions(self, view: sublime.View) -> None:
        self._request_completions(view, REQ_GET_COMPLETIONS, no_callback=True)
        self._request_completions(view, REQ_GET_COMPLETIONS_CYCLING)

    def _request_completions(self, view: sublime.View, request: str, *, no_callback: bool = False) -> None:
        completion_manager = ViewCompletionManager(view)
        completion_manager.hide()

        has_signed_in, is_authorized = self.get_account_status()
        session = self.weaksession()
        sel = view.sel()
        if not (has_signed_in and is_authorized and session and len(sel) == 1):
            return

        params = prepare_completion_request(view)
        if not params:
            return

        if no_callback:
            callback = lambda _: None  # noqa: E731
        else:
            completion_manager.is_waiting = True
            callback = functools.partial(self._on_get_completions, view, region=sel[0].to_tuple())

        session.send_request_async(Request(request, params), callback)

    def _on_get_completions(
        self,
        view: sublime.View,
        payload: CopilotPayloadCompletions,
        region: Tuple[int, int],
    ) -> None:
        completion_manager = ViewCompletionManager(view)
        completion_manager.is_waiting = False

        session = self.weaksession()
        if not session:
            return

        sel = view.sel()
        if len(sel) != 1:
            return

        # re-request completions because the cursor position changed during awaiting Copilot's response
        if sel[0].to_tuple() != region:
            self.request_get_completions(view)
            return

        completions = payload["completions"]
        if not completions:
            return

        preprocess_completions(view, completions)
        completion_manager.show(completions, 0, get_session_setting(session, "completion_style"))
