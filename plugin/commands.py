from __future__ import annotations

import os
import uuid
from abc import ABC
from collections.abc import Callable
from functools import partial, wraps
from pathlib import Path
from typing import Any, Literal, cast

import sublime
import sublime_plugin
from LSP.plugin import Request, Session
from LSP.plugin.core.registry import LspTextCommand, LspWindowCommand
from LSP.plugin.core.url import filename_to_uri
from lsp_utils.helpers import rmtree_ex

from .client import CopilotPlugin
from .constants import (
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
    REQ_FILE_CHECK_STATUS,
    REQ_GET_PANEL_COMPLETIONS,
    REQ_GET_VERSION,
    REQ_NOTIFY_ACCEPTED,
    REQ_NOTIFY_REJECTED,
    REQ_SIGN_IN_CONFIRM,
    REQ_SIGN_IN_INITIATE,
    REQ_SIGN_IN_WITH_GITHUB_TOKEN,
    REQ_SIGN_OUT,
)
from .decorators import _must_be_active_view
from .helpers import (
    GithubInfo,
    prepare_completion_request,
    preprocess_chat_message,
    preprocess_message_for_html,
)
from .types import (
    CopilotPayloadConversationTemplate,
    CopilotPayloadFileStatus,
    CopilotPayloadGetVersion,
    CopilotPayloadNotifyAccepted,
    CopilotPayloadNotifyRejected,
    CopilotPayloadPanelCompletionSolutionCount,
    CopilotPayloadSignInConfirm,
    CopilotPayloadSignInInitiate,
    CopilotPayloadSignOut,
    CopilotRequestCoversationAgent,
    T_Callable,
)
from .ui import ViewCompletionManager, ViewPanelCompletionManager, WindowConversationManager
from .utils import (
    find_index_by_key_value,
    find_view_by_id,
    find_window_by_id,
    get_session_setting,
    message_dialog,
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

    @_must_be_active_view(failed_return=False)
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
        message_dialog("Server version: {}", payload["version"])


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


class CopilotConversationChatShimCommand(LspWindowCommand):
    def run(self, window_id: int, message: str = "") -> None:
        if not (window := find_window_by_id(window_id)):
            return

        wcm = WindowConversationManager(window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return

        view.run_command("copilot_conversation_chat", {"message": message})


class CopilotConversationChatCommand(LspTextCommand):
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
        self, plugin: CopilotPlugin, session: Session, payload, initial_message: str
    ) -> None:
        if not (window := self.view.window()):
            return

        wcm = WindowConversationManager(window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return

        user_prompts = session.config.settings.get("prompts") or {}
        is_template, msg = preprocess_chat_message(view, initial_message, user_prompts)
        if msg:
            wcm.append_conversation_entry({
                "kind": plugin.get_account_status().user or "user",
                "conversationId": wcm.conversation_id,
                "reply": msg.split()[0] if is_template else preprocess_message_for_html(msg),
                "turnId": str(uuid.uuid4()),
                "annotations": [],
                "hideText": False,
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

    def _on_result_conversation_create(self, plugin: CopilotPlugin, session: Session, payload) -> None:
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
        user_prompts = session.config.settings.get("prompts") or {}
        is_template, msg = preprocess_chat_message(view, msg, user_prompts)
        wcm.append_conversation_entry({
            "kind": plugin.get_account_status().user or "user",
            "conversationId": wcm.conversation_id,
            "reply": msg.split()[0] if is_template else preprocess_message_for_html(msg),
            "turnId": str(uuid.uuid4()),
            "annotations": [],
            "hideText": False,
        })

        if not (request := prepare_completion_request(view)):
            return

        session.send_request(
            Request(
                REQ_CONVERSATION_TURN,
                {
                    "conversationId": wcm.conversation_id,
                    "message": msg,
                    "workDoneToken": f"copilot_chat://{wcm.window.id()}",
                    "doc": request["doc"],
                    "computeSuggestions": True,
                    "references": [],
                    "source": "panel",
                },
            ),
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


class CopilotConversationRatingShimCommand(LspWindowCommand):
    def run(self, turn_id: str, rating: int) -> None:
        wcm = WindowConversationManager(self.window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return
        view.run_command("copilot_conversation_rating", {"turn_id": turn_id, "rating": rating})


class CopilotConversationRatingCommand(LspTextCommand):
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
            self._on_result_coversation_rating,
        )

    def _on_result_coversation_rating(self, payload: Literal["OK"]) -> None:
        # Returns OK
        pass


class CopilotConversationDestroyShimCommand(LspWindowCommand):
    def run(self, conversation_id: str) -> None:
        wcm = WindowConversationManager(self.window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return
        view.run_command("copilot_conversation_destroy", {"conversation_id": conversation_id})


class CopilotConversationDestroyCommand(LspTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit, conversation_id: str) -> None:
        if not (
            (window := self.view.window())
            and (wcm := WindowConversationManager(window))
            and wcm.conversation_id == conversation_id
        ):
            return

        session.send_request(
            Request(
                REQ_CONVERSATION_DESTROY,
                {
                    "conversationId": conversation_id,
                    "options": {},
                },
            ),
            self._on_result_coversation_destroy,
        )

    def _on_result_coversation_destroy(self, payload) -> None:
        if not (window := self.view.window()):
            return
        if payload != "OK":
            status_message("Failed to destroy conversation.")
            return

        status_message("Destroyed conversation.")
        wcm = WindowConversationManager(window)
        wcm.close()
        wcm.reset()

    def is_enabled(self, event: dict[Any, Any] | None = None, point: int | None = None) -> bool:
        if not (window := self.view.window()):
            return False
        return super().is_enabled() and bool(WindowConversationManager(window).conversation_id)


class CopilotConversationTurnDeleteShimCommand(LspWindowCommand):
    def run(self, window_id: int, conversation_id: str, turn_id: str) -> None:
        wcm = WindowConversationManager(self.window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return
        view.run_command(
            "copilot_conversation_turn_delete",
            {"window_id": window_id, "conversation_id": conversation_id, "turn_id": turn_id},
        )


class CopilotConversationTurnDeleteCommand(LspTextCommand):
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
            lambda x: self._on_result_coversation_turn_delete(window_id, conversation_id, turn_id, x),
        )

    def _on_result_coversation_turn_delete(self, window_id: int, conversation_id: str, turn_id: str, payload) -> None:
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


class CopilotConversationCopyCodeCommand(LspWindowCommand):
    def run(self, window_id: int, code_block_index: int) -> None:
        if not (window := find_window_by_id(window_id)):
            return

        wcm = WindowConversationManager(window)
        if not (code := wcm.code_block_index.get(str(code_block_index), None)):
            return

        sublime.set_clipboard(code)


class CopilotConversationInsertCodeShimCommand(LspWindowCommand):
    def run(self, window_id: int, code_block_index: int) -> None:
        if not (window := find_window_by_id(window_id)):
            return

        wcm = WindowConversationManager(window)
        if not (view := find_view_by_id(wcm.last_active_view_id)):
            return

        if not (code := wcm.code_block_index.get(str(code_block_index), None)):
            return

        view.run_command("copilot_conversation_insert_code", {"characters": code})


class CopilotConversationInsertCodeCommand(LspTextCommand):
    def run(self, edit: sublime.Edit, characters: str) -> None:
        if len(self.view.sel()) > 1:
            return

        begin = self.view.sel()[0].begin()
        self.view.erase(edit, self.view.sel()[0])
        self.view.insert(edit, begin, characters)


class CopilotConversationAgentsCommand(LspTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(Request(REQ_CONVERSATION_AGENTS, {"options": {}}), self._on_result_coversation_agents)

    def _on_result_coversation_agents(self, payload: list[CopilotRequestCoversationAgent]) -> None:
        window = self.view.window()
        if not window:
            return
        window.show_quick_panel([[item["slug"], item["description"]] for item in payload], lambda _: None)


class CopilotConversationTemplatesCommand(LspTextCommand):
    @_provide_plugin_session()
    def run(self, plugin: CopilotPlugin, session: Session, _: sublime.Edit) -> None:
        session.send_request(
            Request(REQ_CONVERSATION_TEMPLATES, {"options": {}}), self._on_result_conversation_templates
        )

    def _on_result_conversation_templates(self, payload: list[CopilotPayloadConversationTemplate]) -> None:
        if not (window := self.view.window()):
            return
        window.show_quick_panel(
            [[item["id"], item["description"], ", ".join(item["scopes"])] for item in payload],
            lambda index: self._on_selected(index, payload),
        )

    def _on_selected(self, index: int, items: list[CopilotPayloadConversationTemplate]) -> None:
        if index == -1:
            return
        self.view.run_command("copilot_conversation_chat", {"message": f'/{items[index]["id"]}'})


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
        if not (params := prepare_completion_request(self.view)):
            return

        vcm = ViewPanelCompletionManager(self.view)
        vcm.is_waiting = True
        vcm.is_visible = True
        vcm.completions = []

        params["panelId"] = vcm.panel_id
        session.send_request(Request(REQ_GET_PANEL_COMPLETIONS, params), self._on_result_get_panel_completions)

    def _on_result_get_panel_completions(self, payload: CopilotPayloadPanelCompletionSolutionCount) -> None:
        count = payload["solutionCountTarget"]
        status_message("retrieving panel completions: {}", count)

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
            message_dialog("Your GitHub account doesn't subscribe to Copilot.", is_error_=True)
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
        status_message("File is {} in session", payload["status"])


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
            message_dialog(f"Failed to find the session directory: {session_dir}", _error=True)
            return

        rmtree_ex(str(session_dir), ignore_errors=True)
        if not session_dir.is_dir():
            CopilotPlugin.set_account_status(signed_in=False, authorized=False, user=None)
            message_dialog("Sign out OK. Bye!")

        GithubInfo.clear_avatar()
