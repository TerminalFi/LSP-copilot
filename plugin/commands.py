# TODO
# e.set("context/registerProviders", RGe),
# e.set("context/unregisterProviders", Uje),
# e.set("conversation/registerTools", BWe),
# e.set("copilot/codeReview", LWe),
# e.set("git/commitGenerate", yGe),
# e.set("editConversation/create", MWe),
# e.set("editConversation/turn", OWe),
# e.set("editConversation/turnDelete", UWe),
# e.set("editConversation/destroy", QWe),
# e.set("mcp/getTools", qWe),
# e.set("mcp/updateToolsStatus", WWe),

from __future__ import annotations

import json
import os
import subprocess
import uuid
from abc import ABC
from collections.abc import Callable
from functools import partial, wraps
from pathlib import Path
from typing import Any, Literal, Sequence, cast

import sublime
import sublime_plugin
from LSP.plugin import Request, Session
from LSP.plugin.core.registry import LspTextCommand, LspWindowCommand
from LSP.plugin.core.url import filename_to_uri
from lsp_utils.helpers import rmtree_ex

from .client import CopilotPlugin
from .constants import (
    COPILOT_OUTPUT_PANEL_PREFIX,
    PACKAGE_NAME,
    REQ_CHECK_STATUS,
    REQ_CONVERSATION_AGENTS,
    REQ_CONVERSATION_CREATE,
    REQ_CONVERSATION_DESTROY,
    REQ_CONVERSATION_PRECONDITIONS,
    REQ_CONVERSATION_RATING,
    REQ_CONVERSATION_TEMPLATES,
    REQ_CONVERSATION_TURN,
    REQ_CONVERSATION_TURN_DELETE,
    REQ_COPILOT_MODELS,
    REQ_COPILOT_SET_MODEL_POLICY,
    REQ_FILE_CHECK_STATUS,
    REQ_GET_PANEL_COMPLETIONS,
    REQ_GET_PROMPT,
    REQ_GET_VERSION,
    REQ_NOTIFY_ACCEPTED,
    REQ_NOTIFY_REJECTED,
    REQ_SIGN_IN_CONFIRM,
    REQ_SIGN_IN_INITIATE,
    REQ_SIGN_IN_WITH_GITHUB_TOKEN,
    REQ_SIGN_OUT,
    REQ_COPILOT_CODE_REVIEW,
    REQ_GIT_COMMIT_GENERATE,
    REQ_EDIT_CONVERSATION_CREATE,
    REQ_EDIT_CONVERSATION_TURN,
    REQ_EDIT_CONVERSATION_TURN_DELETE,
    REQ_CONVERSATION_REGISTER_TOOLS,
)
from .decorators import must_be_active_view
from .helpers import (
    GithubInfo,
    prepare_completion_request_doc,
    prepare_code_review_request_doc,
    prepare_conversation_turn_request,
    preprocess_chat_message,
    preprocess_message_for_html,
)
from .log import log_info
from .types import (
    CopilotConversationDebugTemplates,
    CopilotModel,
    CopilotPayloadConversationCreate,
    CopilotPayloadConversationPreconditions,
    CopilotPayloadConversationTemplate,
    CopilotPayloadFileStatus,
    CopilotPayloadGetVersion,
    CopilotPayloadNotifyAccepted,
    CopilotPayloadNotifyRejected,
    CopilotPayloadPanelCompletionSolutionCount,
    CopilotPayloadSignInConfirm,
    CopilotPayloadSignInInitiate,
    CopilotPayloadSignOut,
    CopilotRequestConversationAgent,
    CopilotUserDefinedPromptTemplates,
    T_Callable,
    CopilotPayloadEditConversationCreate,
    CopilotPayloadEditConversationTurn,
)
from .ui import ViewCompletionManager, ViewPanelCompletionManager, WindowConversationManager
from .utils import (
    find_index_by_key_value,
    find_view_by_id,
    find_window_by_id,
    get_session_setting,
    message_dialog,
    mutable_view,
    ok_cancel_dialog,
    status_message,
)

REQUIRE_NOTHING = 0
REQUIRE_SIGN_IN = 1 << 0
REQUIRE_NOT_SIGN_IN = 1 << 1
REQUIRE_AUTHORIZED = 1 << 2


def _provide_plugin_session(*, failed_return: Any = None) -> Callable[[T_Callable], T_Callable]:
    """
    The first argument is always `self` for a decorated method.
    We want to provide `plugin` and `session` right after it. If we failed to find a `session`,
    then it will be early failed and return `failed_return`.
    """

    def decorator(func: T_Callable) -> T_Callable:
        @wraps(func)
        def wrapped(self: Any, *arg, **kwargs) -> Any:
            if not isinstance(self, (LspTextCommand)):
                raise RuntimeError('"_provide_session" decorator is only for LspTextCommand.')

            plugin, session = CopilotPlugin.plugin_session(self.view)
            if not (plugin and session):
                return failed_return

            return func(self, plugin, session, *arg, **kwargs)

        return cast(T_Callable, wrapped)

    return decorator


class CopilotPrepareAndEditSettingsCommand(sublime_plugin.ApplicationCommand):
    def run(self, *, base_file: str, user_file: str, default: str = "") -> None:
        window = sublime.active_window()
        user_file_resolved: str = sublime.expand_variables(user_file, window.extract_variables())  # type: ignore
        Path(user_file_resolved).parent.mkdir(parents=True, exist_ok=True)
        sublime.run_command("edit_settings", {"base_file": base_file, "user_file": user_file, "default": default})


class BaseCopilotCommand(ABC):
    session_name = PACKAGE_NAME
    requirement = REQUIRE_SIGN_IN | REQUIRE_AUTHORIZED

    def _can_meet_requirement(self, session: Session) -> bool:
        if get_session_setting(session, "debug"):
            return True

        account_status = CopilotPlugin.get_account_status()
        return not (
            ((self.requirement & REQUIRE_SIGN_IN) and not account_status.has_signed_in)
            or ((self.requirement & REQUIRE_NOT_SIGN_IN) and account_status.has_signed_in)
            or ((self.requirement & REQUIRE_AUTHORIZED) and not account_status.is_authorized)
        )


class CopilotTextCommand(BaseCopilotCommand, LspTextCommand, ABC):
    def want_event(self) -> bool:
        return False

    def _record_telemetry(
        self,
        session: Session,
        request: str,
        payload: CopilotPayloadNotifyAccepted | CopilotPayloadNotifyRejected,
    ) -> None:
        if not get_session_setting(session, "telemetry"):
            return

        session.send_request(Request(request, payload), lambda _: None)

    @must_be_active_view(failed_return=False)
    @_provide_plugin_session(failed_return=False)
    def is_enabled(self, plugin: CopilotPlugin, session: Session) -> bool:  # type: ignore
        return self._can_meet_requirement(session)


class CopilotWindowCommand(BaseCopilotCommand, LspWindowCommand, ABC):
    def is_enabled(self) -> bool:
        if not (session := self.session()):
            return False
        return self._can_meet_requirement(session)


class CopilotGetVersionCommand(CopilotTextCommand):
    requirement = REQUIRE_NOTHING

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_GET_VERSION, {}), self._on_result_get_version)

    def _on_result_get_version(self, payload: CopilotPayloadGetVersion) -> None:
        message_dialog(f"Server version: {payload['version']}")


class CopilotAskCompletionsCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        plugin.request_get_completions(self.view)


class CopilotAcceptPanelCompletionShimCommand(CopilotWindowCommand):
    def run(self, view_id: int, completion_index: int) -> None:
        if not (view := find_view_by_id(view_id)):
            return
        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command("copilot_accept_panel_completion", {"completion_index": completion_index})


class CopilotAcceptPanelCompletionCommand(CopilotTextCommand):
    def run(self, edit: sublime.Edit, completion_index: int) -> None:
        vcm = ViewPanelCompletionManager(self.view)
        if not (completion := vcm.get_completion(completion_index)):
            return

        # it seems that `completionText` always assume your cursor is at the end of the line
        source_line_region = self.view.line(sublime.Region(*completion["region"]))
        self.view.insert(edit, source_line_region.end(), completion["completionText"])
        self.view.show(self.view.sel(), show_surrounds=False, animate=self.view.settings().get("animation_enabled"))

        vcm.close()


class CopilotClosePanelCompletionCommand(CopilotWindowCommand):
    def run(self, view_id: int | None = None) -> None:
        if view_id is None:
            view = self.window.active_view()
        else:
            view = find_view_by_id(view_id)

        if not view:
            return

        ViewPanelCompletionManager(view).close()


class CopilotConversationChatShimCommand(CopilotWindowCommand):
    def run(self, window_id: int, message: str = "") -> None:
        if not (window := find_window_by_id(window_id)):
            return

        wcm = WindowConversationManager(window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return

        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command("copilot_conversation_chat", {"message": message})


class CopilotToggleConversationChatCommand(CopilotWindowCommand):
    def run(self) -> None:
        if not (wcm := WindowConversationManager(self.window)):
            return

        if wcm.is_visible:
            wcm.close()
        elif view := self.window.active_view():
            view.run_command("copilot_conversation_chat")


class CopilotConversationChatCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, message: str = "") -> None:
        if not (window := self.view.window()):
            return

        wcm = WindowConversationManager(window)
        if wcm.conversation_id:
            wcm.open()
            wcm.prompt(callback=lambda msg: self._on_prompt(plugin, session, msg), initial_text=message)
            return

        session.send_request(
            Request(
                REQ_CONVERSATION_PRECONDITIONS,
                {},
            ),
            lambda response: self._on_result_conversation_preconditions(plugin, session, response, message),
        )

    def _on_result_conversation_preconditions(
        self,
        plugin: CopilotPlugin,
        session: Session,
        payload: CopilotPayloadConversationPreconditions,
        initial_message: str,
    ) -> None:
        if not (window := self.view.window()):
            return

        wcm = WindowConversationManager(window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return

        user_prompts: list[CopilotUserDefinedPromptTemplates] = session.config.settings.get("prompts") or []
        is_template, msg = preprocess_chat_message(view, initial_message, user_prompts)
        if msg:
            wcm.append_conversation_entry({
                "kind": plugin.get_account_status().user or "user",
                "conversationId": wcm.conversation_id,
                "reply": msg.split()[0] if is_template else preprocess_message_for_html(msg),
                "turnId": str(uuid.uuid4()),
                "references": [],
                "annotations": [],
                "hideText": False,
                "warnings": [],
            })
        session.send_request(
            Request(
                REQ_CONVERSATION_CREATE,
                {
                    "turns": [{"request": msg}],
                    "capabilities": {
                        "allSkills": True,
                        "skills": [],
                    },
                    "workDoneToken": f"copilot_chat://{window.id()}",
                    "computeSuggestions": True,
                    "source": "panel",
                },
            ),
            lambda msg: self._on_result_conversation_create(plugin, session, msg),
        )
        wcm.is_waiting = True
        wcm.update()

    def _on_result_conversation_create(
        self,
        plugin: CopilotPlugin,
        session: Session,
        payload: CopilotPayloadConversationCreate,
    ) -> None:
        if not (window := self.view.window()):
            return

        wcm = WindowConversationManager(window)
        wcm.conversation_id = payload["conversationId"]
        wcm.open()
        wcm.prompt(callback=lambda msg: self._on_prompt(plugin, session, msg))

    def _on_prompt(self, plugin: CopilotPlugin, session: Session, msg: str):
        if not (window := self.view.window()):
            return

        wcm = WindowConversationManager(window)
        if wcm.is_waiting:
            wcm.prompt(callback=lambda x: self._on_prompt(plugin, session, x), initial_text=msg)
            return

        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return
        user_prompts: list[CopilotUserDefinedPromptTemplates] = session.config.settings.get("prompts") or []
        is_template, msg = preprocess_chat_message(view, msg, user_prompts)
        views = [sv.view for sv in session.session_views_async() if sv.view.id() != view.id()]
        if not (request := prepare_conversation_turn_request(wcm.conversation_id, wcm.window.id(), msg, view, views)):
            return

        wcm.append_conversation_entry({
            "kind": plugin.get_account_status().user or "user",
            "conversationId": wcm.conversation_id,
            "reply": msg.split()[0] if is_template else preprocess_message_for_html(msg),
            "turnId": str(uuid.uuid4()),
            "references": request["references"],
            "annotations": [],
            "hideText": False,
            "warnings": [],
        })
        session.send_request(
            Request(REQ_CONVERSATION_TURN, request),
            lambda _: wcm.prompt(callback=lambda x: self._on_prompt(plugin, session, x)),
        )
        wcm.is_waiting = True
        wcm.update()


class CopilotConversationCloseCommand(CopilotWindowCommand):
    def run(self, window_id: int | None = None) -> None:
        if not window_id:
            return
        if not (window := find_window_by_id(window_id)):
            return

        WindowConversationManager(window).close()


class CopilotConversationRatingShimCommand(CopilotWindowCommand):
    def run(self, turn_id: str, rating: int) -> None:
        wcm = WindowConversationManager(self.window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return
        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command("copilot_conversation_rating", {"turn_id": turn_id, "rating": rating})


class CopilotConversationRatingCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, turn_id: str, rating: int) -> None:
        session.send_request(
            Request(
                REQ_CONVERSATION_RATING,
                {
                    "turnId": turn_id,
                    "rating": rating,
                },
            ),
            self._on_result_conversation_rating,
        )

    def _on_result_conversation_rating(self, payload: Literal["OK"]) -> None:
        # Returns OK
        pass

    def is_enabled(self, event: dict[Any, Any] | None = None, point: int | None = None) -> bool:  # type: ignore
        return True


class CopilotConversationDestroyShimCommand(CopilotWindowCommand):
    def run(self, conversation_id: str) -> None:
        wcm = WindowConversationManager(self.window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            status_message("Failed to find last active view.")
            return
        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command("copilot_conversation_destroy", {"conversation_id": conversation_id})


class CopilotConversationDestroyCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, conversation_id: str) -> None:
        if not (
            (window := self.view.window())
            and (wcm := WindowConversationManager(window))
            and wcm.conversation_id == conversation_id
        ):
            status_message("Failed to find window or conversation.")
            return

        session.send_request(
            Request(
                REQ_CONVERSATION_DESTROY,
                {
                    "conversationId": conversation_id,
                    "options": {},
                },
            ),
            self._on_result_conversation_destroy,
        )

    def _on_result_conversation_destroy(self, payload: str) -> None:
        if not (window := self.view.window()):
            status_message("Failed to find window")
            return
        if payload != "OK":
            status_message("Failed to destroy conversation.")
            return

        status_message("Destroyed conversation.")
        wcm = WindowConversationManager(window)
        wcm.close()
        wcm.reset()

    def is_enabled(self, event: dict[Any, Any] | None = None, point: int | None = None) -> bool:  # type: ignore
        if not (window := self.view.window()):
            return False
        return bool(WindowConversationManager(window).conversation_id)


class CopilotConversationToggleReferencesBlockCommand(CopilotWindowCommand):
    def run(self, window_id: int, conversation_id: str, turn_id: str) -> None:
        wcm = WindowConversationManager(self.window)
        if conversation_id != wcm.conversation_id:
            return

        wcm.toggle_references_block(turn_id)
        wcm.update()


class CopilotConversationTurnDeleteShimCommand(CopilotWindowCommand):
    def run(self, window_id: int, conversation_id: str, turn_id: str) -> None:
        wcm = WindowConversationManager(self.window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return
        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command(
            "copilot_conversation_turn_delete",
            {"window_id": window_id, "conversation_id": conversation_id, "turn_id": turn_id},
        )


class CopilotConversationTurnDeleteCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(
        self,
        plugin: CopilotPlugin,
        session: Session,
        _: sublime.Edit,
        window_id: int,
        conversation_id: str,
        turn_id: str,
    ) -> None:
        if not (window := find_window_by_id(window_id)):
            return

        wcm = WindowConversationManager(window)
        if wcm.conversation_id != conversation_id:
            return

        # Fixes: https://github.com/TerminalFi/LSP-copilot/issues/181
        index = find_index_by_key_value(wcm.conversation, "turnId", turn_id) + 1
        if index >= len(wcm.conversation):
            return
        retrieved_turn_id = wcm.conversation[index]["turnId"]

        session.send_request(
            Request(
                REQ_CONVERSATION_TURN_DELETE,
                {
                    "conversationId": conversation_id,
                    "turnId": retrieved_turn_id,
                    "options": {},
                },
            ),
            lambda x: self._on_result_conversation_turn_delete(window_id, conversation_id, turn_id, x),
        )

    def _on_result_conversation_turn_delete(
        self,
        window_id: int,
        conversation_id: str,
        turn_id: str,
        payload: str,
    ) -> None:
        if payload != "OK":
            status_message("Failed to delete turn.")
            return

        if not (window := find_window_by_id(window_id)):
            return

        wcm = WindowConversationManager(window)
        if wcm.conversation_id != conversation_id:
            return

        index = find_index_by_key_value(wcm.conversation, "turnId", turn_id)
        conversation = wcm.conversation
        del conversation[index:]
        wcm.follow_up = ""
        wcm.conversation = conversation
        wcm.update()

    def is_enabled(self, event: dict[Any, Any] | None = None, point: int | None = None) -> bool:  # type: ignore
        return True


class CopilotConversationCopyCodeCommand(CopilotWindowCommand):
    def run(self, window_id: int, code_block_index: int) -> None:
        if not (window := find_window_by_id(window_id)):
            return

        wcm = WindowConversationManager(window)
        if not (code := wcm.code_block_index.get(str(code_block_index), None)):
            return

        sublime.set_clipboard(code)


class CopilotConversationInsertCodeShimCommand(CopilotWindowCommand):
    def run(self, window_id: int, code_block_index: int) -> None:
        if not (window := find_window_by_id(window_id)):
            status_message(f"Failed to find window based on ID. ({window_id})")
            return

        wcm = WindowConversationManager(window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            status_message("Window has no active view")
            return

        if not (code := wcm.code_block_index.get(str(code_block_index), None)):
            status_message(f"Failed to find code based on index. {code_block_index}")
            return

        # Focus the view so that the command runs
        self.window.focus_view(view)
        view.run_command("copilot_conversation_insert_code", {"characters": code})


class CopilotConversationInsertCodeCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, characters: str) -> None:
        if len(self.view.sel()) > 1:
            return

        begin = self.view.sel()[0].begin()
        self.view.erase(edit, self.view.sel()[0])
        self.view.insert(edit, begin, characters)


class CopilotConversationAgentsCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_CONVERSATION_AGENTS, {}), self._on_result_conversation_agents)

    def _on_result_conversation_agents(self, payload: list[CopilotRequestConversationAgent]) -> None:
        for agent in payload:
            print(agent["slug"], agent["name"], agent["description"])


class CopilotRegisterConversationToolsCommand(CopilotTextCommand):
    """Command to register custom tools for Copilot Chat conversations."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        # Define tools to register
        tools = [
            {
                "id": "sublime-file-search",
                "name": "Search Files in Sublime",
                "description": "Search for files in the current project or workspace",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        },
                        "maxResults": {
                            "type": "integer",
                            "description": "Maximum number of results to return"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "id": "sublime-text-search",
                "name": "Search Text in Sublime",
                "description": "Search for text content across files in the project",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The text to search for"
                        },
                        "filePattern": {
                            "type": "string",
                            "description": "Optional file pattern to limit search"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]

        # Send request to register tools
        session.send_request(
            Request(
                REQ_CONVERSATION_REGISTER_TOOLS,
                {
                    "tools": tools
                }
            ),
            self._on_result_register_tools
        )

        status_message("Registering conversation tools...", icon="⏳")

    def _on_result_register_tools(self, payload: Any) -> None:
        if isinstance(payload, dict) and payload.get("status") == "OK":
            status_message("Successfully registered conversation tools", icon="✅")
        else:
            status_message("Failed to register conversation tools", icon="❌")


class CopilotModelsCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_COPILOT_MODELS, {}), self._on_result_copilot_models)

    def _on_result_copilot_models(self, payload: list[CopilotModel]) -> None:
        window = self.view.window() or sublime.active_window()
        window.show_quick_panel(
            [
                sublime.QuickPanelItem(
                    trigger=item["modelFamily"],
                    details=item["modelName"],
                    annotation=", ".join(item["scopes"]),
                )
                for item in payload
            ],
            lambda index: self._set_model_policy(index, payload),
        )

    def _set_model_policy(self, index: int, models: list[CopilotModel]) -> None:
        if index == -1:
            return
        model_name = models[index]["modelFamily"]
        self.view.run_command("copilot_set_model_policy", {"model": model_name, "status": "enabled"})


class CopilotCodeReviewCommand(CopilotTextCommand):
    """Command to perform code review using GitHub Copilot."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        if not (window := self.view.window()):
            return

        # Get the file URI for the current view
        file_uri = filename_to_uri(self.view.file_name() or "")
        if not file_uri:
            status_message("Cannot perform code review on an unsaved file", icon="❌")
            return
        doc = prepare_code_review_request_doc(self.view)
        sublime.set_clipboard(json.dumps(doc))
        # Send request to perform code review
        session.send_request(
            Request(
                REQ_COPILOT_CODE_REVIEW,
                {
                    "uri": file_uri,
                    "document": doc,
                    "selection": doc["selection"],
                    "source": "command_palette",
                }
            ),
            lambda response: self._on_result_code_review(response, window)
        )

        status_message("Analyzing code...", icon="⏳")

    def _on_result_code_review(self, payload: dict, window: sublime.Window) -> None:
        """Handle the code review response from Copilot."""
        if not payload:
            status_message("Code review failed or returned no results", icon="❌")
            return

        # Create an output panel to show the review results
        panel_name = f"{COPILOT_OUTPUT_PANEL_PREFIX}_code_review"
        panel = window.create_output_panel(panel_name)
        panel.set_read_only(False)
        panel.run_command("append", {"characters": "# GitHub Copilot Code Review\n\n"})

        # Process review comments if available
        if comments := payload.get("comments", []):
            for i, comment in enumerate(comments, 1):
                # Extract comment details
                message = comment.get("message", "No message provided")
                kind = comment.get("kind", "unknown")
                severity = comment.get("severity", "unknown")

                # Format the comment header
                panel.run_command("append", {"characters": f"## Comment {i} ({kind.title()} - {severity.title()})\n\n"})
                panel.run_command("append", {"characters": f"{message}\n\n"})

                # Add line range information if available
                if file_range := comment.get("range"):
                    line_start = file_range.get("start", {}).get("line", 0) + 1
                    line_end = file_range.get("end", {}).get("line", 0) + 1
                    char_start = file_range.get("start", {}).get("character", 0)
                    char_end = file_range.get("end", {}).get("character", 0)

                    if line_start == line_end:
                        panel.run_command("append", {"characters": f"**Location:** Line {line_start}, characters {char_start}-{char_end}\n\n"})
                    else:
                        panel.run_command("append", {"characters": f"**Location:** Lines {line_start}-{line_end}\n\n"})

                # Add file information if different from current file
                if uri := comment.get("uri"):
                    import urllib.parse
                    file_path = urllib.parse.unquote(uri.replace("file://", ""))
                    file_name = file_path.split("/")[-1] if "/" in file_path else file_path
                    panel.run_command("append", {"characters": f"**File:** {file_name}\n\n"})

                panel.run_command("append", {"characters": "---\n\n"})
        else:
            panel.run_command("append", {"characters": "No issues found in your code. Great job! ✅\n\n"})

        panel.set_read_only(True)
        window.run_command("show_panel", {"panel": f"output.{panel_name}"})
        status_message("Code review completed", icon="✅")


class CopilotGitCommitGenerateCommand(CopilotTextCommand):
    """Command to generate Git commit messages using GitHub Copilot."""

    def _run_git_command(self, cmd: list[str], cwd: str | None = None) -> str | None:
        """Run a git command and return the output, or None if it fails."""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=10,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def _get_git_repo_root(self, start_path: str) -> str | None:
        """Find the Git repository root starting from the given path."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=start_path,
                capture_output=True,
                text=True,
                timeout=5,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def _get_git_changes(self, repo_root: str) -> list[str]:
        """Get actual diff content for staged and unstaged changes."""
        changes = []

        # Get staged changes (actual diff content)
        staged_output = self._run_git_command(["git", "diff", "--cached"], repo_root)
        if staged_output:
            changes.append(f"=== STAGED CHANGES ===\n{staged_output}")

        # Get unstaged changes (actual diff content)
        unstaged_output = self._run_git_command(["git", "diff"], repo_root)
        if unstaged_output:
            changes.append(f"=== UNSTAGED CHANGES ===\n{unstaged_output}")

        # Get untracked files content (for small files)
        untracked_output = self._run_git_command(["git", "ls-files", "--others", "--exclude-standard"], repo_root)
        if untracked_output:
            untracked_files = [f.strip() for f in untracked_output.split('\n') if f.strip()]
            untracked_content = []

            for file_path in untracked_files[:5]:  # Limit to first 5 untracked files
                full_path = Path(repo_root) / file_path
                try:
                    if full_path.is_file() and full_path.stat().st_size < 10000:  # Only read files < 10KB
                        content = full_path.read_text(encoding='utf-8', errors='ignore')
                        untracked_content.append(f"=== NEW FILE: {file_path} ===\n{content}")
                except (OSError, UnicodeDecodeError):
                    untracked_content.append(f"=== NEW FILE: {file_path} ===\n[Binary or unreadable file]")

            if untracked_content:
                changes.extend(untracked_content)

        return changes

    def _get_current_user_email(self, repo_root: str) -> str | None:
        """Get the current Git user email."""
        return self._run_git_command(["git", "config", "user.email"], repo_root)

    def _get_user_commits(self, repo_root: str, user_email: str | None, limit: int = 10) -> list[str]:
        """Get recent commits by the current user."""
        if not user_email:
            return []

        cmd = [
            "git", "log",
            f"--author={user_email}",
            f"--max-count={limit}",
            "--oneline",
            "--no-merges"
        ]

        output = self._run_git_command(cmd, repo_root)
        if output:
            return [line.strip() for line in output.split('\n') if line.strip()]
        return []

    def _get_recent_commits(self, repo_root: str, limit: int = 20) -> list[str]:
        """Get recent commits from all contributors."""
        cmd = [
            "git", "log",
            f"--max-count={limit}",
            "--oneline",
            "--no-merges"
        ]

        output = self._run_git_command(cmd, repo_root)
        if output:
            return [line.strip() for line in output.split('\n') if line.strip()]
        return []

    def _get_workspace_folder(self) -> str | None:
        """Get the workspace folder path."""
        if not (window := self.view.window()):
            return None

        # Try to get the project path
        if folders := window.folders():
            return folders[0]

        # Fallback to file directory
        if file_name := self.view.file_name():
            return str(Path(file_name).parent)

        return None

    def _get_user_language(self) -> str | None:
        """Get user's language preference from Sublime Text settings."""
        # Try to get language from various Sublime Text settings
        settings = sublime.load_settings("Preferences.sublime-settings")

        # Check for explicit language setting
        if lang := settings.get("language"):
            return lang

        # Fallback to system locale
        try:
            import locale
            return locale.getdefaultlocale()[0]
        except:
            return "en-US"

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        if not (window := self.view.window()):
            return

        # Get workspace folder
        workspace_folder = self._get_workspace_folder()
        if not workspace_folder:
            status_message("No workspace folder found", icon="❌")
            return

        # Find Git repository root
        repo_root = self._get_git_repo_root(workspace_folder)
        if not repo_root:
            status_message("Not in a Git repository", icon="❌")
            return

        # Gather Git information
        changes = self._get_git_changes(repo_root)
        user_email = self._get_current_user_email(repo_root)
        user_commits = self._get_user_commits(repo_root, user_email)
        recent_commits = self._get_recent_commits(repo_root)
        user_language = self._get_user_language()

        # Prepare payload according to expected structure
        payload = {
            "changes": changes,
            "userCommits": user_commits,
            "recentCommits": recent_commits,
            "workspaceFolder": workspace_folder,
            "userLanguage": user_language,
        }

        status_message("Generating commit message...", icon="⏳")

        # Send request to generate commit message
        session.send_request(
            Request(REQ_GIT_COMMIT_GENERATE, payload),
            lambda response: self._on_result_git_commit_generate(response, window)
        )

    def _on_result_git_commit_generate(self, payload: dict, window: sublime.Window) -> None:
        """Handle the git commit message generation response from Copilot."""
        if not payload or not (commit_message := payload.get("message")):
            status_message("Failed to generate commit message", icon="❌")
            return

        # Create a new view for the commit message
        view = window.new_file()
        view.set_name("Git Commit Message")
        view.set_scratch(True)

        # Insert the generated commit message
        with mutable_view(view) as we:
            we.replace(sublime.Region(0, view.size()), commit_message)

        # Set commit message syntax
        view.assign_syntax("Packages/Git/Git Commit.sublime-syntax")

        status_message("Commit message generated", icon="✅")


class CopilotSetModelPolicyCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, model: str, status: str) -> None:
        session.send_request(
            Request(REQ_COPILOT_SET_MODEL_POLICY, {"model": model, "status": status}),
            lambda _: None,
        )


class CopilotGetPromptCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        doc = prepare_completion_request_doc(self.view)
        session.send_request(Request(REQ_GET_PROMPT, {"doc": doc}), self._on_result_get_prompt)

    def _on_result_get_prompt(self, payload) -> None:
        if not (window := self.view.window()):
            return
        view = window.create_output_panel(f"{COPILOT_OUTPUT_PANEL_PREFIX}.prompt_view", unlisted=True)
        view.assign_syntax("scope:source.json")

        with mutable_view(view) as view:
            view.run_command("append", {"characters": json.dumps(payload, indent=4)})
        window.run_command("show_panel", {"panel": f"output.{COPILOT_OUTPUT_PANEL_PREFIX}.prompt_view"})


class CopilotConversationTemplatesCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        user_prompts: list[CopilotUserDefinedPromptTemplates] = session.config.settings.get("prompts") or []
        session.send_request(
            Request(REQ_CONVERSATION_TEMPLATES, {"options": {}}),
            lambda payload: self._on_result_conversation_templates(user_prompts, payload),
        )

    def _on_result_conversation_templates(
        self,
        user_prompts: list[CopilotUserDefinedPromptTemplates],
        payload: list[CopilotPayloadConversationTemplate],
    ) -> None:
        if not (window := self.view.window()):
            return

        templates = payload + user_prompts
        prompts = [
            [
                item["id"],
                item["description"],
                ", ".join(item["scopes"]) if item.get("scopes") else "chat-panel",
            ]
            for item in templates
        ]
        window.show_quick_panel(
            prompts,
            lambda index: self._on_selected(index, templates),
        )

    def _on_selected(
        self,
        index: int,
        items: list[CopilotPayloadConversationTemplate | CopilotUserDefinedPromptTemplates],
    ) -> None:
        if index == -1:
            return
        self.view.run_command("copilot_conversation_chat", {"message": f"/{items[index]['id']}"})


class CopilotAcceptCompletionCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, edit: sublime.Edit) -> None:
        if not (vcm := ViewCompletionManager(self.view)).is_visible:
            return

        vcm.hide()
        if not (completion := vcm.current_completion):
            return

        # Remove the current line and then insert full text.
        # We don't have to care whether it's an inline completion or not.
        source_line_region = self.view.line(completion["point"])
        self.view.erase(edit, source_line_region)
        self.view.insert(edit, source_line_region.begin(), completion["text"])
        self.view.show(self.view.sel(), show_surrounds=False, animate=self.view.settings().get("animation_enabled"))

        self._record_telemetry(session, REQ_NOTIFY_ACCEPTED, {"uuid": completion["uuid"]})

        other_uuids = [completion["uuid"] for completion in vcm.completions]
        other_uuids.remove(completion["uuid"])
        if other_uuids:
            self._record_telemetry(session, REQ_NOTIFY_REJECTED, {"uuids": other_uuids})


class CopilotRejectCompletionCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        vcm = ViewCompletionManager(self.view)
        vcm.hide()

        self._record_telemetry(
            session,
            REQ_NOTIFY_REJECTED,
            {"uuids": [completion["uuid"] for completion in vcm.completions]},
        )


class CopilotGetPanelCompletionsCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        if not (doc := prepare_completion_request_doc(self.view)):
            return

        vcm = ViewPanelCompletionManager(self.view)
        vcm.is_waiting = True
        vcm.is_visible = True
        vcm.completions = []

        params = {"doc": doc, "panelId": vcm.panel_id}
        session.send_request(Request(REQ_GET_PANEL_COMPLETIONS, params), self._on_result_get_panel_completions)

    def _on_result_get_panel_completions(self, payload: CopilotPayloadPanelCompletionSolutionCount) -> None:
        count = payload["solutionCountTarget"]
        status_message(f"retrieving panel completions: {count}")

        ViewPanelCompletionManager(self.view).open(completion_target_count=count)


class CopilotPreviousCompletionCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        ViewCompletionManager(self.view).show_previous_completion()


class CopilotNextCompletionCommand(CopilotTextCommand):
    def run(self, _: sublime.Edit) -> None:
        ViewCompletionManager(self.view).show_next_completion()


class CopilotCheckStatusCommand(CopilotTextCommand):
    requirement = REQUIRE_NOTHING

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        local_checks = get_session_setting(session, "local_checks")
        session.send_request(Request(REQ_CHECK_STATUS, {"localChecksOnly": local_checks}), self._on_result_check_status)

    def _on_result_check_status(self, payload: CopilotPayloadSignInConfirm | CopilotPayloadSignOut) -> None:
        if not ((user := payload.get("user")) and isinstance(user, str)):
            user = ""

        CopilotPlugin.set_account_status(user=user)
        GithubInfo.update_avatar(user)

        if payload["status"] == "OK":
            CopilotPlugin.set_account_status(signed_in=True, authorized=True)
            message_dialog(f'Signed in and authorized with user "{user}".')
        elif payload["status"] == "MaybeOk":
            CopilotPlugin.set_account_status(signed_in=True, authorized=True)
            message_dialog(f'(localChecksOnly) Signed in and authorized with user "{user}".')
        elif payload["status"] == "NotAuthorized":
            CopilotPlugin.set_account_status(signed_in=True, authorized=False)
            message_dialog("Your GitHub account doesn't subscribe to Copilot.", error=True)
        else:
            CopilotPlugin.set_account_status(signed_in=False, authorized=False)
            message_dialog("You haven't signed in yet.")


class CopilotCheckFileStatusCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        file_path = self.view.file_name() or ""
        uri = file_path and filename_to_uri(file_path)
        session.send_request(Request(REQ_FILE_CHECK_STATUS, {"uri": uri}), self._on_result_check_file_status)

    def _on_result_check_file_status(self, payload: CopilotPayloadFileStatus) -> None:
        status_message(f"File is {payload['status']} in session")


class CopilotSignInCommand(CopilotTextCommand):
    requirement = REQUIRE_NOT_SIGN_IN

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(
            Request(REQ_SIGN_IN_INITIATE, {}),
            partial(self._on_result_sign_in_initiate, session),
        )

    def _on_result_sign_in_initiate(
        self,
        session: Session,
        payload: CopilotPayloadSignInConfirm | CopilotPayloadSignInInitiate,
    ) -> None:
        if payload["status"] == "AlreadySignedIn":
            return
        CopilotPlugin.set_account_status(signed_in=False, authorized=False, quiet=True)

        user_code = str(payload.get("userCode", ""))
        verification_uri = str(payload.get("verificationUri", ""))
        if not (user_code and verification_uri):
            return
        sublime.set_clipboard(user_code)
        sublime.run_command("open_url", {"url": verification_uri})
        log_info(f"Sign-in URL: {verification_uri} (User code = {user_code})")
        if not ok_cancel_dialog(
            "The device activation code has been copied."
            + " Please paste it in the popup GitHub page. Press OK when completed."
            + " If you don't see a popup GitHub page, please check Sublime Text's console,"
            + " open the given URL and paste the user code manually.",
        ):
            return
        session.send_request(
            Request(REQ_SIGN_IN_CONFIRM, {"userCode": user_code}),
            self._on_result_sign_in_confirm,
        )

    def _on_result_sign_in_confirm(self, payload: CopilotPayloadSignInConfirm) -> None:
        self.view.run_command("copilot_check_status")


class CopilotSignInWithGithubTokenCommand(CopilotTextCommand):
    requirement = REQUIRE_NOT_SIGN_IN

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(
            Request(REQ_SIGN_IN_INITIATE, {}),
            partial(self._on_result_sign_in_initiate, session),
        )

    def _on_result_sign_in_initiate(
        self,
        session: Session,
        payload: CopilotPayloadSignInConfirm | CopilotPayloadSignInInitiate,
    ) -> None:
        if payload["status"] == "AlreadySignedIn":
            return
        CopilotPlugin.set_account_status(signed_in=False, authorized=False, quiet=True)

        if not (window := self.view.window()):
            return

        window.show_input_panel(
            "Github Username",
            "",
            on_done=lambda username: self._on_select_github_username(session, username),
            on_change=None,
            on_cancel=None,
        )

    def _on_select_github_username(self, session: Session, username: str) -> None:
        if not (window := self.view.window()):
            return

        window.show_input_panel(
            "Github Token",
            "ghu_",
            on_done=lambda token: session.send_request(
                Request(REQ_SIGN_IN_WITH_GITHUB_TOKEN, {"githubToken": token, "user": username}),
                self._on_result_sign_in_confirm,
            ),
            on_change=None,
            on_cancel=None,
        )

    def _on_result_sign_in_confirm(self, payload: CopilotPayloadSignInConfirm) -> None:
        self.view.run_command("copilot_check_status")


class CopilotSignOutCommand(CopilotTextCommand):
    requirement = REQUIRE_SIGN_IN

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_SIGN_OUT, {}), self._on_result_sign_out)

    def _on_result_sign_out(self, payload: CopilotPayloadSignOut) -> None:
        if sublime.platform() == "windows":
            session_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "github-copilot"
        else:
            session_dir = Path.home() / ".config/github-copilot"

        if not session_dir.is_dir():
            message_dialog(f"Failed to find the session directory: {session_dir}", error=True)
            return

        rmtree_ex(str(session_dir), ignore_errors=True)
        if not session_dir.is_dir():
            CopilotPlugin.set_account_status(signed_in=False, authorized=False, user=None)
            message_dialog("Sign out OK. Bye!")

        GithubInfo.clear_avatar()


class CopilotConversationDebugCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        if not (window := self.view.window()):
            return

        templates = tuple(CopilotConversationDebugTemplates)
        window.show_quick_panel(
            [[template.name, template.value] for template in templates],
            lambda index: self._on_selected(index, templates),
        )

    def _on_selected(self, index: int, templates: Sequence[CopilotConversationDebugTemplates]) -> None:
        if index == -1:
            return
        self.view.run_command("copilot_conversation_chat", {"message": f"{templates[index].value}"})


class CopilotSendAnyRequestCommand(CopilotTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, request_type: str, payload: str) -> None:
        try:
            decode_payload = sublime.decode_value(payload)
        except ValueError as e:
            message_dialog(f"Failed to parse payload: {e}", error=True)
            decode_payload = {}
        session.send_request(Request(request_type, decode_payload), self._on_results_any_request)

    def _on_results_any_request(self, payload: Any) -> None:
        print(payload)

    def input(self, args: dict[str, Any]) -> sublime_plugin.CommandInputHandler | None:
        return CopilotSendAnyRequestCommandTextInputHandler()


class CopilotSendAnyRequestCommandTextInputHandler(sublime_plugin.TextInputHandler):
    def placeholder(self) -> str:
        return "Enter type of request. Example: conversation/turn"

    def name(self) -> str:
        return "request_type"

    def next_input(self, args: dict[str, Any]) -> sublime_plugin.CommandInputHandler | None:
        return CopilotSendAnyRequestPayloadInputHandler(args)


class CopilotSendAnyRequestPayloadInputHandler(sublime_plugin.TextInputHandler):
    def __init__(self, args: dict[str, Any]) -> None:
        self.args = args

    def placeholder(self) -> str:
        return 'Enter payload JSON. Example: {"conversationId": "12345"}'

    def name(self) -> str:
        return "payload"

# THIS IS NOT IMPLEMENTED
class CopilotEditConversationCreateCommand(CopilotTextCommand):
    """Command to create a new edit conversation with GitHub Copilot."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        if not (window := self.view.window()):
            return

        file_uri = filename_to_uri(self.view.file_name() or "")
        if not file_uri:
            status_message("Cannot start edit conversation on an unsaved file", icon="❌")
            return

        # Prepare the initial document information for the edit conversation
        doc = prepare_completion_request_doc(self.view)

        # Send request to create a new edit conversation
        session.send_request(
            Request(
                REQ_EDIT_CONVERSATION_CREATE,
                {
                    "doc": doc,
                    "turns": [{"request": "Help me improve this code\n\n```python\n\ndef example_function():\n    pass\n```"}],
                    "capabilities": {
                        "editingSupport": True,
                        "editingOptions": ["refactor", "explain", "fix", "document"]
                    },
                    "partialResultToken": f"copilot_pedit://{window.id()}",
                    "editConversationId": f"copilot_edit://{window.id()}",
                    "source": "panel",
                }
            ),
            lambda response: self._on_result_edit_conversation_create(plugin, session, response)
        )

        status_message("Creating edit conversation...", icon="⏳")

    def _on_result_edit_conversation_create(
        self,
        plugin: CopilotPlugin,
        session: Session,
        payload: CopilotPayloadEditConversationCreate,
    ) -> None:
        if not (window := self.view.window()):
            return

        # Store the conversation ID for later use
        conversation_id = payload["conversationId"]

        # Create an output panel to display the edit conversation
        panel_name = f"{COPILOT_OUTPUT_PANEL_PREFIX}_edit_{conversation_id[:8]}"
        panel = window.create_output_panel(panel_name)
        panel.set_read_only(False)
        panel.run_command("append", {"characters": "# Copilot Edit Conversation\n\n"})
        panel.run_command("append", {"characters": "Ready to help you edit this code. What would you like to do?\n\n"})
        panel.run_command("append", {"characters": "Options: refactor, explain, fix, document\n\n"})
        panel.set_read_only(True)

        # Show the panel
        window.run_command("show_panel", {"panel": f"output.{panel_name}"})

        # Store conversation data in view settings
        panel.settings().set(f"{COPILOT_WINDOW_SETTINGS_PREFIX}.edit_conversation_id", conversation_id)
        panel.settings().set(f"{COPILOT_WINDOW_SETTINGS_PREFIX}.edit_source_view_id", self.view.id())

        # Prompt user for input
        window.show_input_panel(
            "Copilot Edit:",
            "",
            lambda msg: self._on_prompt_input(plugin, session, conversation_id, msg, panel),
            None,
            None
        )

    def _on_prompt_input(
        self,
        plugin: CopilotPlugin,
        session: Session,
        conversation_id: str,
        message: str,
        panel: sublime.View
    ) -> None:
        if not message.strip():
            return

        if not (window := self.view.window()):
            return

        # Get the source view
        source_view_id = panel.settings().get(f"{COPILOT_WINDOW_SETTINGS_PREFIX}.edit_source_view_id")
        source_view = find_view_by_id(source_view_id)
        if not source_view:
            status_message("Source view no longer available", icon="❌")
            return

        # Update the panel with the user's message
        panel.set_read_only(False)
        panel.run_command("append", {"characters": f"## You\n\n{message}\n\n"})
        panel.set_read_only(True)

        # Prepare the document for the request
        doc = prepare_completion_request_doc(source_view)

        # Send the turn request
        session.send_request(
            Request(
                REQ_EDIT_CONVERSATION_TURN,
                {
                    "conversationId": conversation_id,
                    "message": message,
                    "doc": doc,
                    "workDoneToken": f"copilot_edit://{window.id()}_{conversation_id}",
                    "editOptions": {
                        "allowAutoEdit": True
                    },
                    "source": "panel"
                }
            ),
            lambda response: self._on_result_edit_conversation_turn(panel, source_view, response)
        )

        status_message("Processing edit request...", icon="⏳")

    def _on_result_edit_conversation_turn(
        self,
        panel: sublime.View,
        source_view: sublime.View,
        payload: CopilotPayloadEditConversationTurn
    ) -> None:
        if not payload.get("reply"):
            status_message("No response from Copilot", icon="❌")
            return

        # Update the panel with the assistant's response
        panel.set_read_only(False)
        panel.run_command("append", {"characters": f"## Copilot\n\n{payload['reply']}\n\n"})

        # Check if the response includes code edits
        if edits := payload.get("edits", []):
            panel.run_command("append", {"characters": "Edits available. Use 'Apply Edit' to apply them.\n\n"})

            # Store edits in the panel's settings
            panel.settings().set(f"{COPILOT_WINDOW_SETTINGS_PREFIX}.pending_edits", edits)

            # Add a clickable link to apply edits
            panel.run_command("append", {"characters": "[Apply Edit](command:copilot_apply_edit_conversation_edits)\n\n"})

        panel.set_read_only(True)

        # Show the panel in case it was closed
        if window := panel.window():
            window.run_command("show_panel", {"panel": f"output.{panel.settings().get('output.name')}"})

        # Continue the conversation
        window.show_input_panel(
            "Copilot Edit:",
            "",
            lambda msg: self._on_prompt_input(None, None, payload["conversationId"], msg, panel),
            None,
            None
        )


class CopilotApplyEditConversationEditsCommand(CopilotTextCommand):
    """Command to apply edits from an edit conversation."""

    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, edit: sublime.Edit) -> None:
        # This command should be run from the panel, but we need to apply edits to the source view
        if not (window := self.view.window()):
            return

        # Get pending edits and source view ID from settings
        pending_edits = self.view.settings().get(f"{COPILOT_WINDOW_SETTINGS_PREFIX}.pending_edits", [])
        source_view_id = self.view.settings().get(f"{COPILOT_WINDOW_SETTINGS_PREFIX}.edit_source_view_id")

        if not pending_edits:
            status_message("No pending edits to apply", icon="❌")
            return

        # Get the source view
        source_view = find_view_by_id(source_view_id)
        if not source_view:
            status_message("Source view no longer available", icon="❌")
            return

        # Apply edits to the source view
        window.focus_view(source_view)
        with mutable_view(source_view) as edit_obj:
            for edit_item in pending_edits:
                if range_data := edit_item.get("range"):
                    # Convert LSP range to Sublime Text region
                    start_point = source_view.text_point(
                        range_data["start"]["line"],
                        range_data["start"]["character"]
                    )
                    end_point = source_view.text_point(
                        range_data["end"]["line"],
                        range_data["end"]["character"]
                    )
                    region = sublime.Region(start_point, end_point)

                    # Replace the text in the region
                    edit_obj.replace(region, edit_item.get("newText", ""))

        # Clear pending edits
        self.view.settings().erase(f"{COPILOT_WINDOW_SETTINGS_PREFIX}.pending_edits")
        status_message("Applied edits to the document", icon="✅")


class CopilotEditConversationTurnDeleteCommand(CopilotTextCommand):
    """Command to delete a turn from an edit conversation."""

    @_provide_plugin_session()
    def run(
        self,
        plugin: CopilotPlugin,
        session: Session,
        _: sublime.Edit,
        conversation_id: str,
        turn_id: str
    ) -> None:
        session.send_request(
            Request(
                REQ_EDIT_CONVERSATION_TURN_DELETE,
                {
                    "conversationId": conversation_id,
                    "turnId": turn_id
                }
            ),
            lambda response: self._on_result_edit_conversation_turn_delete(conversation_id, turn_id, response)
        )

    def _on_result_edit_conversation_turn_delete(
        self,
        conversation_id: str,
        turn_id: str,
        payload: Any
    ) -> None:
        status_message(f"Deleted turn from edit conversation", icon="✅")

        # Update the panel if it exists
        if not (window := self.view.window()):
            return

        panel_name = f"{COPILOT_OUTPUT_PANEL_PREFIX}_edit_{conversation_id[:8]}"
        for view in window.views():
            if view.settings().get('output.name') == panel_name:
                view.run_command("copilot_refresh_edit_conversation_panel", {"conversation_id": conversation_id})
                break


class CopilotRefreshEditConversationPanelCommand(sublime_plugin.TextCommand):
    """Command to refresh the edit conversation panel."""

    def run(self, edit: sublime.Edit, conversation_id: str) -> None:
        # This is a utility command to update the panel after deleting a turn
        # In a real implementation, this would fetch the updated conversation
        # and redraw the panel contents
        self.view.set_read_only(False)
        self.view.run_command("append", {"characters": "\n[Turn deleted]\n\n"})
        self.view.set_read_only(True)
