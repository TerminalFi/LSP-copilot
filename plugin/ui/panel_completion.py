from __future__ import annotations

import textwrap
from collections.abc import Iterable

import mdpopups
import sublime
from more_itertools import first_true, unique_everseen

from ..types import CopilotPayloadPanelSolution, StLayout
from ..utils import (
    all_views,
    find_view_by_id,
    fix_completion_syntax_highlight,
    get_copilot_view_setting,
    get_view_language_id,
    reformat,
    remove_prefix,
    set_copilot_view_setting,
)


class ViewPanelCompletionManager:
    # ------------- #
    # view settings #
    # ------------- #

    @property
    def is_visible(self) -> bool:
        """Whether the panel completions is visible."""
        return get_copilot_view_setting(self.view, "is_visible_panel_completions", False)

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "is_visible_panel_completions", value)

    @property
    def is_waiting(self) -> bool:
        """Whether the panel completions synthesis has been done."""
        return get_copilot_view_setting(self.view, "is_waiting_panel_completions", False)

    @is_waiting.setter
    def is_waiting(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "is_waiting_panel_completions", value)

    @property
    def group_id(self) -> int:
        """The ID of the group which is used to show panel completions."""
        return get_copilot_view_setting(self.view, "panel_group_id", -1)

    @group_id.setter
    def group_id(self, value: int) -> None:
        set_copilot_view_setting(self.view, "panel_group_id", value)

    @property
    def sheet_id(self) -> int:
        """The ID of the sheet which is used to show panel completions."""
        return get_copilot_view_setting(self.view, "panel_sheet_id", -1)

    @sheet_id.setter
    def sheet_id(self, value: int) -> None:
        set_copilot_view_setting(self.view, "panel_sheet_id", value)

    @property
    def original_layout(self) -> StLayout | None:
        """The original window layout prior to panel presentation."""
        return get_copilot_view_setting(self.view, "original_layout", None)

    @original_layout.setter
    def original_layout(self, value: StLayout | None) -> None:
        set_copilot_view_setting(self.view, "original_layout", value)

    @property
    def completion_target_count(self) -> int:
        """How many completions are synthesized in panel completions."""
        return get_copilot_view_setting(self.view, "panel_completion_target_count", 0)

    @completion_target_count.setter
    def completion_target_count(self, value: int) -> None:
        set_copilot_view_setting(self.view, "panel_completion_target_count", value)

    @property
    def completions(self) -> list[CopilotPayloadPanelSolution]:
        """All `completions` in the view. Note that this is a copy."""
        return get_copilot_view_setting(self.view, "panel_completions", [])

    @completions.setter
    def completions(self, value: list[CopilotPayloadPanelSolution]) -> None:
        set_copilot_view_setting(self.view, "panel_completions", value)

    @property
    def panel_id(self) -> str:
        """The panel ID sent to Copilot `getPanelCompletions` request."""
        return f"copilot://{self.view.id()}"

    # -------------- #
    # normal methods #
    # -------------- #

    def __init__(self, view: sublime.View) -> None:
        self.view = view

    def reset(self) -> None:
        self.is_waiting = False
        self.is_visible = False
        self.original_layout = None

    def get_completion(self, index: int) -> CopilotPayloadPanelSolution | None:
        try:
            return self.completions[index]
        except IndexError:
            return None

    def append_completion(self, completion: CopilotPayloadPanelSolution) -> None:
        completions = self.completions
        completions.append(completion)
        self.completions = completions

    @staticmethod
    def find_view_by_panel_id(panel_id: str) -> sublime.View | None:
        view_id = int(remove_prefix(panel_id, "copilot://"))
        return find_view_by_id(view_id)

    @classmethod
    def from_sheet_id(cls, sheet_id: int) -> ViewPanelCompletionManager | None:
        return first_true(map(cls, all_views()), pred=lambda self: self.sheet_id == sheet_id)

    def open(self, *, completion_target_count: int | None = None) -> None:
        """Open the completion panel."""
        if completion_target_count is not None:
            self.completion_target_count = completion_target_count

        _PanelCompletion(self.view).open()

    def update(self) -> None:
        """Update the completion panel."""
        _PanelCompletion(self.view).update()

    def close(self) -> None:
        """Close the completion panel."""
        _PanelCompletion(self.view).close()


class _PanelCompletion:
    CSS_CLASS_NAME = "copilot-completion-panel"
    CSS = f"""
        html {{
            --copilot-close-foreground: var(--foreground);
            --copilot-close-background: var(--background);
            --copilot-close-border: var(--foreground);
            --copilot-accept-foreground: var(--foreground);
            --copilot-accept-background: var(--background);
            --copilot-accept-border: var(--greenish);
        }}

        .{CSS_CLASS_NAME} {{
            margin: 1rem 0.5rem 0 0.5rem;
        }}

        .{CSS_CLASS_NAME} .navbar {{
            text-align: left;
        }}

        .{CSS_CLASS_NAME} .synthesis-info {{
            display: inline-block;
            text-size: 1.2em;
        }}

        .{CSS_CLASS_NAME} .header {{
            display: block;
            margin-bottom: 1rem;
        }}

        .{CSS_CLASS_NAME} a {{
            border-radius: 3px;
            border-style: solid;
            border-width: 1px;
            display: inline;
            padding: 5px;
            text-decoration: none;
        }}

        .{CSS_CLASS_NAME} a.close {{
            background: var(--copilot-close-background);
            border-color: var(--copilot-close-border);
            color: var(--copilot-close-foreground);
        }}

        .{CSS_CLASS_NAME} a.close i {{
            color: var(--copilot-close-border);
        }}

        .{CSS_CLASS_NAME} a.accept {{
            background: var(--copilot-accept-background);
            border-color: var(--copilot-accept-border);
            color: var(--copilot-accept-foreground);
        }}

        .{CSS_CLASS_NAME} a.accept i {{
            color: var(--copilot-accept-border);
        }}
        """
    COMPLETION_TEMPLATE = reformat("""
        <div class="navbar">
            <a class="close" title="Close Completion Panel" href='{close_panel}'><i>×</i> Close</a>&nbsp;
            <h4 class="synthesis-info">{synthesis_info}</h4>
        </div>
        <hr>
        {sections}
    """)
    # We use many backticks to denote a fenced code block because if we are writing in Markdown,
    # Copilot may suggest 3 backticks for a fenced code block and that can break our templating.
    COMPLETION_SECTION_TEMPLATE = reformat("""
        <div class="header">{header_items}</div>
        ``````{lang}
        {code}
        ``````
    """)

    def __init__(self, view: sublime.View) -> None:
        self.view = view
        self.completion_manager = ViewPanelCompletionManager(view)

    @property
    def completion_content(self) -> str:
        completions = self._synthesize(self.completion_manager.completions)

        if self.completion_manager.is_waiting:
            synthesis_info = "⌛ Synthesizing {index} unique solutions out of {total_solutions}..."
        else:
            synthesis_info = "Synthesized {index} unique solutions out of {total_solutions}. (Done)"

        return self.COMPLETION_TEMPLATE.format(
            close_panel=sublime.command_url("copilot_close_panel_completion", {"view_id": self.view.id()}),
            synthesis_info=synthesis_info.format(
                index=len(completions),
                total_solutions=self.completion_manager.completion_target_count,
            ),
            sections="\n\n<hr>\n".join(
                self.COMPLETION_SECTION_TEMPLATE.format(
                    header_items=" &nbsp;".join(self.completion_header_items(completion, self.view.id(), index)),
                    score=completion["score"],
                    lang=get_view_language_id(self.view, completion["region"][1]),
                    code=fix_completion_syntax_highlight(
                        self.view,
                        completion["region"][1],
                        self._prepare_popup_code_display_text(completion["displayText"]),
                    ),
                )
                for index, completion in completions
            ),
        )

    @staticmethod
    def completion_header_items(completion: CopilotPayloadPanelSolution, view_id: int, index: int) -> list[str]:
        return [
            """<a class="accept" title="Accept Completion" href='{}'><i>✓</i> Accept</a>""".format(
                sublime.command_url(
                    "copilot_accept_panel_completion_shim",
                    {"view_id": view_id, "completion_index": index},
                )
            ),
            # Removing this for now. The response still contains `score` however it
            # is always zero-value
            # "<i>Mean Probability: {}</i>".format(completion["score"]),
        ]

    def open(self) -> None:
        window = self.view.window()
        if not window:
            return

        active_group = window.active_group()
        if active_group == window.num_groups() - 1:
            self._open_in_side_by_side(window)
        else:
            self._open_in_group(window, active_group + 1)

        window.focus_view(self.view)

    def update(self) -> None:
        window = self.view.window()
        if not window:
            return

        sheet = window.transient_sheet_in_group(self.completion_manager.group_id)
        if not isinstance(sheet, sublime.HtmlSheet):
            return

        mdpopups.update_html_sheet(
            sheet=sheet,
            contents=self.completion_content,
            md=True,
            css=self.CSS,
            wrapper_class=self.CSS_CLASS_NAME,
        )

    def close(self) -> None:
        window = self.view.window()
        if not window:
            return

        sheet = window.transient_sheet_in_group(self.completion_manager.group_id)
        if not isinstance(sheet, sublime.HtmlSheet):
            return

        sheet.close()
        self.completion_manager.is_visible = False
        if self.completion_manager.original_layout:
            window.set_layout(self.completion_manager.original_layout)
            self.completion_manager.original_layout = None

        window.focus_view(self.view)

    @staticmethod
    def _prepare_popup_code_display_text(display_text: str) -> str:
        # The returned completion is in the form of
        #   - the first won't be indented
        #   - the rest of lines will be indented basing on the indentation level of the current line
        # The rest of lines don't visually look good if the current line is deeply indented.
        # Hence we modify the rest of lines into always indented by one level if it's originally indented.
        first_line, sep, rest = display_text.partition("\n")

        if rest.startswith((" ", "\t")):
            return first_line + sep + textwrap.indent(textwrap.dedent(rest), "\t")

        return display_text

    @staticmethod
    def _synthesize(
        completions: Iterable[CopilotPayloadPanelSolution],
    ) -> list[tuple[int, CopilotPayloadPanelSolution]]:
        """Return sorted-by-`score` completions in the form of `[(completion_index, completion), ...]`."""
        return sorted(
            # note that we must keep completion's original index
            unique_everseen(enumerate(completions), key=lambda pair: pair[1]["completionText"]),
            key=lambda pair: pair[1]["score"],
            reverse=True,
        )

    def _open_in_group(self, window: sublime.Window, group_id: int) -> None:
        self.completion_manager.group_id = group_id

        window.focus_group(group_id)
        sheet: sublime.HtmlSheet = mdpopups.new_html_sheet(
            window=window,
            name="Panel Completions",
            contents=self.completion_content,
            md=True,
            css=self.CSS,
            flags=sublime.TRANSIENT,
            wrapper_class=self.CSS_CLASS_NAME,
        )
        self.completion_manager.sheet_id = sheet.id()

    def _open_in_side_by_side(self, window: sublime.Window) -> None:
        self.completion_manager.original_layout = window.layout()
        window.set_layout({
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
        })
        self._open_in_group(window, 1)
