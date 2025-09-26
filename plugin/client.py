from __future__ import annotations

import functools
import json
import os
import weakref
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any, cast
from urllib.parse import urlparse
import uuid

import jmespath
import sublime
from LSP.plugin import ClientConfig, DottedDict, Notification, Request, Session, WorkspaceFolder
from lsp_utils import ApiWrapperInterface, NpmClientHandler, notification_handler, request_handler
from LSP.plugin.core.protocol import Point, Range
from LSP.plugin.core.sessions import SessionViewProtocol
from LSP.plugin.core.url import filename_to_uri

from .constants import (
    NTFY_FEATURE_FLAGS_NOTIFICATION,
    NTFY_LOG_MESSAGE,
    NTFY_PANEL_SOLUTION,
    NTFY_PANEL_SOLUTION_DONE,
    NTFY_STATUS_NOTIFICATION,
    PACKAGE_NAME,
    REQ_CHECK_STATUS,
    REQ_CONVERSATION_CONTEXT,
    REQ_GET_COMPLETIONS,
    REQ_GET_COMPLETIONS_CYCLING,
    REQ_GET_VERSION,
    REQ_SET_EDITOR_INFO,
    REQ_CONTEXT_REGISTER_PROVIDERS,
    COPILOT_ACCEPT_SUGGESTION_KINDS,
    COPILOT_OUTPUT_PANEL_PREFIX,
    REQ_CONVERSATION_AGENTS,
    REQ_CONVERSATION_PRECONDITIONS,
    REQ_CONVERSATION_TEMPLATES,
    REQ_GET_PANEL_COMPLETIONS,
    REQ_NOTIFY_SHOWN,
    REQ_COPILOT_MODELS,
    EDIT_STATUS_BEGIN,
    EDIT_STATUS_END,
    EDIT_STATUS_PLAN_GENERATED,
    EDIT_STATUS_OVERALL_DESCRIPTION,
    EDIT_STATUS_CODE_GENERATED,
    EDIT_STATUS_NO_CODE_BLOCKS,
)
from .helpers import (
    ActivityIndicator,
    CopilotIgnore,
    GithubInfo,
    prepare_completion_request_doc,
    preprocess_completions,
    preprocess_panel_completions,
)
from .log import log_warning, log_info, log_debug
from .template import load_string_template
from .types import (
    AccountStatus,
    CopilotPayloadCompletions,
    CopilotPayloadConversationContext,
    CopilotPayloadFeatureFlagsNotification,
    CopilotPayloadGetVersion,
    CopilotPayloadLogMessage,
    CopilotPayloadPanelSolution,
    CopilotPayloadSignInConfirm,
    CopilotPayloadStatusNotification,
    NetworkProxy,
    T_Callable,
    CopilotPayloadNotifyShown,
    CopilotPayloadSetEditorInfo,
    T_AccountStatus,
    T_CompletionItem,
)
from .ui import ViewCompletionManager, ViewPanelCompletionManager, WindowConversationManager, WindowEditConversationManager
from .utils import (
    all_views,
    all_windows,
    debounce,
    get_session_setting,
    status_message,
    find_window_by_id,
)

WindowId = int


@dataclass
class WindowAttr:
    client: CopilotPlugin | None = None
    """The LSP client instance for the window."""


def _guard_view(*, failed_return: Any = None) -> Callable[[T_Callable], T_Callable]:
    """
    The first two arguments have to be `self` and `view` for a decorated method.
    If `view` doesn't meeting some requirements, it will be early failed and return `failed_return`.
    """

    def decorator(func: T_Callable) -> T_Callable:
        @wraps(func)
        def wrapped(self: Any, view: sublime.View, *arg, **kwargs) -> Any:
            view_settings = view.settings()
            if (
                not view.is_valid()
                or view.element()
                or view.is_read_only()
                or view_settings.get("command_mode")
                or view_settings.get("is_widget")
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
        "@github",
        "copilot-language-server",
        "dist",
        "language-server.js",
    )

    server_version = ""
    """The version of the "@github/copilot-language-server" package."""
    server_version_gh = ""
    """The version of the Github Copilot language server."""

    window_attrs: weakref.WeakKeyDictionary[sublime.Window, WindowAttr] = weakref.WeakKeyDictionary()
    """Per-window attributes. I.e., per-session attributes."""

    _account_status = AccountStatus(
        has_signed_in=False,
        is_authorized=False,
    )

    _activity_indicator: ActivityIndicator | None = None

    def __init__(self, session: weakref.ref[Session]) -> None:
        super().__init__(session)

        if sess := session():
            self.window_attrs[sess.window].client = self

        self._activity_indicator = ActivityIndicator(self.update_status_bar_text)

        # Note that ST persists view settings after ST is closed. If the user closes ST
        # during awaiting Copilot's response, the internal state management will be corrupted.
        # So, we have to reset some status when started.
        for view in all_views():
            ViewCompletionManager(view).reset()
            ViewPanelCompletionManager(view).reset()

        for window in all_windows():
            WindowConversationManager(window).reset()

    @classmethod
    def setup(cls) -> None:
        super().setup()

        cls.server_version = cls.parse_server_version()

    @classmethod
    def cleanup(cls) -> None:
        cls.window_attrs.clear()
        super().cleanup()

    @classmethod
    def can_start(
        cls,
        window: sublime.Window,
        initiating_view: sublime.View,
        workspace_folders: list[WorkspaceFolder],
        configuration: ClientConfig,
    ) -> str | None:
        if message := super().can_start(window, initiating_view, workspace_folders, configuration):
            return message

        cls.window_attrs.setdefault(window, WindowAttr())
        return None

    @classmethod
    def on_pre_start(
        cls,
        window: sublime.Window,
        initiating_view: sublime.View,
        workspace_folders: list[WorkspaceFolder],
        configuration: ClientConfig,
    ) -> str | None:
        super().on_pre_start(window, initiating_view, workspace_folders, configuration)
        configuration.init_options.update(cls.editor_info())
        return None

    def on_ready(self, api: ApiWrapperInterface) -> None:
        def _on_get_version(response: CopilotPayloadGetVersion, failed: bool) -> None:
            self.server_version_gh = response.get("version", "")

        def _on_check_status(result: CopilotPayloadSignInConfirm, failed: bool) -> None:
            user = result.get("user")
            self.set_account_status(
                signed_in=result["status"] in {"NotAuthorized", "OK"},
                authorized=result["status"] == "OK",
                user=user,
            )
            
        def _on_register_providers(response: Any, failed: bool) -> None:
            if failed:
                log_warning("Failed to register context providers")
            else:
                log_info("Successfully registered context providers")

        api.send_request(REQ_GET_VERSION, {}, _on_get_version)
        api.send_request(REQ_CHECK_STATUS, {}, _on_check_status)
        
        # Register context providers
        api.send_request(
            REQ_CONTEXT_REGISTER_PROVIDERS,
            {
                "providers": [
                    {
                        "id": "sublime-text-editor",
                        "name": "Sublime Text Editor",
                        "fullName": "Sublime Text Editor Context Provider",
                        "description": "Provides access to the Sublime Text editor context"
                    }
                ]
            },
            _on_register_providers
        )

    def on_settings_changed(self, settings: DottedDict) -> None:
        def parse_proxy(proxy: str) -> NetworkProxy | None:
            # in the form of "username:password@host:port" or "host:port"
            if not proxy:
                return None
            parsed = urlparse(f"http://{proxy}")
            return {
                "host": parsed.hostname or "",
                "port": parsed.port or 80,
                "username": parsed.username or "",
                "password": parsed.password or "",
                "rejectUnauthorized": True,
            }

        super().on_settings_changed(settings)

        if not (session := self.weaksession()):
            return

        editor_info = self.editor_info()

        if networkProxy := parse_proxy(settings.get("proxy") or ""):
            editor_info["networkProxy"] = networkProxy

        session.send_request(Request(REQ_SET_EDITOR_INFO, editor_info), lambda response: None)
        self.update_status_bar_text()

    @staticmethod
    def version() -> str:
        """Return this plugin's version. If it's not installed by Package Control, return `"unknown"`."""
        try:
            return json.loads(sublime.load_resource(f"Packages/{PACKAGE_NAME}/package-metadata.json"))["version"]
        except Exception:
            return "unknown"

    @classmethod
    def editor_info(cls) -> dict[str, Any]:
        return {
            "editorInfo": {
                "name": "vscode",
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
        return ">=18"

    @classmethod
    def get_account_status(cls) -> AccountStatus:
        """Return the account status object."""
        return cls._account_status

    @classmethod
    def set_account_status(
        cls,
        *,
        signed_in: bool | None = None,
        authorized: bool | None = None,
        user: str | None = None,
        quiet: bool = False,
    ) -> None:
        if signed_in is not None:
            cls._account_status.has_signed_in = signed_in
        if authorized is not None:
            cls._account_status.is_authorized = authorized
        if user is not None:
            cls._account_status.user = user
            GithubInfo.fetch_avatar(user)

        if not quiet:
            if not cls._account_status.has_signed_in:
                icon, msg = "❌", "has NOT been signed in."
            elif not cls._account_status.is_authorized:
                icon, msg = "⚠", "has signed in but not authorized."
            else:
                icon, msg = "✈", "has been signed in and authorized."
            status_message(msg, icon=icon, console=True)

    @classmethod
    def from_view(cls, view: sublime.View) -> CopilotPlugin | None:
        if (
            (window := view.window())
            and (window_attr := cls.window_attrs.get(window))
            and (self := window_attr.client)
            and self.is_valid_for_view(view)
        ):
            return self
        return None

    @classmethod
    def parse_server_version(cls) -> str:
        lock_file_content = sublime.load_resource(f"Packages/{PACKAGE_NAME}/language-server/package-lock.json")
        return (
            jmespath.search(
                'dependencies."@github/copilot-language-server".version',
                json.loads(lock_file_content),
            )
            or ""
        )

    @classmethod
    def plugin_session(cls, view: sublime.View) -> tuple[None, None] | tuple[CopilotPlugin, Session | None]:
        plugin = cls.from_view(view)
        return (plugin, plugin.weaksession()) if plugin else (None, None)

    @classmethod
    def should_ignore(cls, view: sublime.View) -> bool:
        if not (window := view.window()):
            return False
        return CopilotIgnore(window).trigger(view)

    def is_valid_for_view(self, view: sublime.View) -> bool:
        session = self.weaksession()
        return bool(session and session.session_view_for_view_async(view))

    def update_status_bar_text(self, extra_variables: dict[str, Any] | None = None) -> None:
        if not (session := self.weaksession()):
            return

        variables: dict[str, Any] = {
            "server_version": self.server_version,
            "server_version_gh": self.server_version_gh,
        }

        if extra_variables:
            variables.update(extra_variables)

        rendered_text = ""
        if template_text := str(session.config.settings.get("status_text") or ""):
            try:
                rendered_text = load_string_template(template_text).render(variables)
            except Exception as e:
                log_warning(f'Invalid "status_text" template: {e}')
        session.set_config_status_async(rendered_text)

    def on_server_notification_async(self, notification: Notification) -> None:
        if notification.method == "$/progress":
            token = notification.params.get("token", "")
            params = notification.params.get("value")
            
            if not params:
                return
                
            if token.startswith("copilot_chat://"):
                self._handle_chat_progress(token, params)
            elif token.startswith("copilot_pedit://"):
                self._handle_edit_progress(token, params)

    def _handle_chat_progress(self, token: str, params: Any) -> None:
        """Handle progress notifications for chat conversations."""
        window = WindowConversationManager.find_window_by_token_id(token)
        if not window:
            return
            
        wcm = WindowConversationManager(window)
        needs_update = False
        
        if params.get("kind") == "end":
            wcm.is_waiting = False
            needs_update = True

        if suggest_title := params.get("suggestedTitle"):
            wcm.suggested_title = suggest_title
            needs_update = True

        if params.get("reply"):
            wcm.append_conversation_entry(params)
            needs_update = True

        if followup := params.get("followUp"):
            wcm.follow_up = followup.get("message", "")
            needs_update = True
            
        if needs_update:
            wcm.update()

    def _handle_edit_progress(self, token: str, params: list[dict[str, Any]]) -> None:
        """Handle progress notifications for edit conversations."""
        window = WindowConversationManager.find_window_by_token_id(token)
        if not window:
            return
            
        wecm = WindowEditConversationManager(window)
        needs_update = False
        
        for update in params:
            if "editConversationId" in update:
                wecm.conversation_id = update["editConversationId"]
                needs_update = True
                
                # Handle different file generation statuses
                status = update.get("fileGenerationStatus")
                if status == EDIT_STATUS_BEGIN:
                    wecm.is_waiting = True
                    wecm.open()
                elif status == EDIT_STATUS_END:
                    wecm.is_waiting = False
                elif status == EDIT_STATUS_NO_CODE_BLOCKS:
                    self._handle_no_code_blocks_response(wecm, update)
                elif status in (EDIT_STATUS_PLAN_GENERATED, EDIT_STATUS_OVERALL_DESCRIPTION):
                    self._handle_edit_description_response(wecm, update)
                elif status == EDIT_STATUS_CODE_GENERATED:
                    self._handle_code_generated_response(wecm, update)
                    
        if needs_update:
            wecm.update()

    def _create_conversation_entry(
        self, 
        conversation_id: str, 
        reply: str, 
        turn_id: str | None = None,
        kind: str = "report"
    ) -> dict[str, Any]:
        """Helper method to create a standardized conversation entry."""
        return {
            "kind": kind,
            "conversationId": conversation_id,
            "reply": reply,
            "turnId": turn_id or str(uuid.uuid4()),
            "references": [],
            "annotations": [],
            "hideText": False,
            "warnings": [],
        }

    def _handle_no_code_blocks_response(self, wecm: WindowEditConversationManager, update: dict[str, Any]) -> None:
        """Handle the no-code-blocks-found response."""
        entry = self._create_conversation_entry(
            wecm.conversation_id,
            update["rawResponse"],
            update.get("editTurnId")
        )
        wecm.append_conversation_entry(entry)
        wecm.is_waiting = False

    def _handle_edit_description_response(self, wecm: WindowEditConversationManager, update: dict[str, Any]) -> None:
        """Handle edit plan or description generated responses."""
        if "editDescription" in update:
            entry = self._create_conversation_entry(
                wecm.conversation_id,
                update["editDescription"],
                update.get("editTurnId")
            )
            wecm.append_conversation_entry(entry)

    def _handle_code_generated_response(self, wecm: WindowEditConversationManager, update: dict[str, Any]) -> None:
        """Handle updated code generated responses."""
        if "partialText" not in update:
            return
            
        # Format the code with proper markdown code fence
        language_id = update.get("languageId", "")
        code_content = update["partialText"]
        markdown_reply = f"```{language_id}\n{code_content}\n```"
        
        # Add conversation entry
        entry = self._create_conversation_entry(
            wecm.conversation_id,
            markdown_reply,
            update.get("editTurnId")
        )
        wecm.append_conversation_entry(entry)
        
        # Add as a pending edit for the entire file
        self._add_full_file_edit(wecm, code_content)

    def _add_full_file_edit(self, wecm: WindowEditConversationManager, code_content: str) -> None:
        """Add a pending edit that replaces the entire file content."""
        source_view = wecm.get_source_view()
        if not source_view:
            return
            
        # Calculate the range for the entire file
        file_content = source_view.substr(sublime.Region(0, source_view.size()))
        lines = file_content.split('\n')
        last_line = len(lines) - 1
        last_char = len(lines[-1]) if lines else 0
        
        wecm.add_pending_edit({
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": last_line, "character": last_char}
            },
            "newText": code_content
        })

    @notification_handler(NTFY_FEATURE_FLAGS_NOTIFICATION)
    def _handle_feature_flags_notification(self, payload: CopilotPayloadFeatureFlagsNotification) -> None:
        pass

    @notification_handler(NTFY_LOG_MESSAGE)
    def _handle_log_message_notification(self, payload: CopilotPayloadLogMessage) -> None:
        pass

    @notification_handler(NTFY_PANEL_SOLUTION)
    def _handle_panel_solution_notification(self, payload: CopilotPayloadPanelSolution) -> None:
        if not (view := ViewPanelCompletionManager.find_view_by_panel_id(payload["panelId"])):
            return

        preprocess_panel_completions(view, [payload])

        vcm = ViewPanelCompletionManager(view)
        vcm.append_completion(payload)
        vcm.update()

    @notification_handler(NTFY_PANEL_SOLUTION_DONE)
    def _handle_panel_solution_done_notification(self, payload) -> None:
        if not (view := ViewPanelCompletionManager.find_view_by_panel_id(payload["panelId"])):
            return

        vcm = ViewPanelCompletionManager(view)
        vcm.is_waiting = False
        vcm.update()

    @notification_handler(NTFY_STATUS_NOTIFICATION)
    def _handle_status_notification_notification(self, payload: CopilotPayloadStatusNotification) -> None:
        pass

    @request_handler(REQ_CONVERSATION_CONTEXT)
    def _handle_conversation_context_request(
        self,
        payload: CopilotPayloadConversationContext,
        respond: Callable[[Any], None],
    ) -> None:
        respond(None)  # what?

    @_guard_view()
    @debounce()
    def request_get_completions(self, view: sublime.View) -> None:
        self._request_completions(view, REQ_GET_COMPLETIONS, no_callback=True)
        self._request_completions(view, REQ_GET_COMPLETIONS_CYCLING)

    def _request_completions(self, view: sublime.View, request: str, *, no_callback: bool = False) -> None:
        vcm = ViewCompletionManager(view)
        vcm.hide()

        if not (
            (session := self.weaksession())
            and self._account_status.has_signed_in
            and self._account_status.is_authorized
            and len(sel := view.sel()) == 1
        ):
            return

        if not (doc := prepare_completion_request_doc(view)):
            return

        if no_callback:
            callback = lambda _: None  # noqa: E731
        else:
            vcm.is_waiting = True
            if self._activity_indicator:
                self._activity_indicator.start()
            callback = functools.partial(self._on_get_completions, view, region=sel[0].to_tuple())

        session.send_request_async(Request(request, {"doc": doc}), callback)

    def _on_get_completions(
        self,
        view: sublime.View,
        payload: CopilotPayloadCompletions,
        region: tuple[int, int],
    ) -> None:
        vcm = ViewCompletionManager(view)
        vcm.is_waiting = False
        if self._activity_indicator:
            self._activity_indicator.stop()

        if not (session := self.weaksession()):
            return

        if len(sel := view.sel()) != 1:
            return

        # re-request completions because the cursor position changed during awaiting Copilot's response
        if sel[0].to_tuple() != region:
            self.request_get_completions(view)
            return

        if not (completions := payload["completions"]):
            return

        preprocess_completions(view, completions)
        vcm.show(completions, 0, get_session_setting(session, "completion_style"))

    @notification_handler(REQ_NOTIFY_SHOWN)
    def _handle_notify_shown_notification(self, payload: CopilotPayloadNotifyShown) -> None:
        pass

    @notification_handler(REQ_COPILOT_MODELS)
    def _handle_copilot_models_notification(self, payload: Any) -> None:
        pass

    @notification_handler(REQ_CONVERSATION_AGENTS)
    def _handle_conversation_agents_notification(self, payload: Any) -> None:
        pass

    @notification_handler(REQ_CONVERSATION_PRECONDITIONS)
    def _handle_conversation_preconditions_notification(self, payload: Any) -> None:
        pass

    @notification_handler(REQ_CONVERSATION_TEMPLATES)
    def _handle_conversation_templates_notification(self, payload: Any) -> None:
        pass

    @notification_handler(REQ_GET_PANEL_COMPLETIONS)
    def _handle_get_panel_completions_notification(self, payload: Any) -> None:
        pass

    @notification_handler(EDIT_STATUS_BEGIN)
    def _handle_edit_status_begin_notification(self, payload: Any) -> None:
        pass

    @notification_handler(EDIT_STATUS_END)
    def _handle_edit_status_end_notification(self, payload: Any) -> None:
        pass

    @notification_handler(EDIT_STATUS_PLAN_GENERATED)
    def _handle_edit_status_plan_generated_notification(self, payload: Any) -> None:
        pass

    @notification_handler(EDIT_STATUS_OVERALL_DESCRIPTION)
    def _handle_edit_status_overall_description_notification(self, payload: Any) -> None:
        pass

    @notification_handler(EDIT_STATUS_CODE_GENERATED)
    def _handle_edit_status_code_generated_notification(self, payload: Any) -> None:
        pass

    @notification_handler(EDIT_STATUS_NO_CODE_BLOCKS)
    def _handle_edit_status_no_code_blocks_notification(self, payload: Any) -> None:
        pass
