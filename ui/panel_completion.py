import textwrap
from operator import itemgetter

import mdpopups
import sublime
from LSP.plugin.core.typing import Iterable, List, Optional

from ..types import CopilotPayloadPanelSolution
from ..utils import (
    erase_copilot_view_setting,
    find_sheet_by_group,
    find_view_by_id,
    get_copilot_view_setting,
    get_view_language_id,
    reformat,
    remove_prefix,
    set_copilot_view_setting,
    unique,
    mdpopups_update_html_sheet,
)


class ViewPanelCompletionManager:
    # ------------- #
    # view settings #
    # ------------- #

    @property
    def group_id(self) -> int:
        """The ID of the group which is used to show panel completions."""
        return get_copilot_view_setting(self.view, "panel_group_id", -1)

    @group_id.setter
    def group_id(self, value: int) -> None:
        set_copilot_view_setting(self.view, "panel_group_id", value)

    @property
    def is_waiting(self) -> bool:
        return get_copilot_view_setting(self.view, "is_waiting_panel_completions", False)

    @is_waiting.setter
    def is_waiting(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "is_waiting_panel_completions", value)

    @property
    def sheet_id(self) -> int:
        """The ID of the sheet which is used to show panel completions."""
        return get_copilot_view_setting(self.view, "panel_sheet_id", -1)

    @sheet_id.setter
    def sheet_id(self, value: int) -> None:
        set_copilot_view_setting(self.view, "panel_sheet_id", value)

    @property
    def original_layout(self):
        """The Original window layout prior to panel presentation."""
        return get_copilot_view_setting(self.view, "original_layout", {})

    @original_layout.setter
    def original_layout(self, value) -> None:
        set_copilot_view_setting(self.view, "original_layout", value)

    @property
    def completion_target_count(self) -> int:
        return get_copilot_view_setting(self.view, "panel_completion_target_count", 0)

    @completion_target_count.setter
    def completion_target_count(self, value: int) -> None:
        set_copilot_view_setting(self.view, "panel_completion_target_count", value)

    @property
    def panel_id(self) -> str:
        return "copilot://{}".format(self.view.id())

    @property
    def completions(self) -> List[CopilotPayloadPanelSolution]:
        """All `completions` in the view. Note that this is a copy."""
        return get_copilot_view_setting(self.view, "panel_completions", [])

    @completions.setter
    def completions(self, value: List[CopilotPayloadPanelSolution]) -> None:
        set_copilot_view_setting(self.view, "panel_completions", value)

    # -------------- #
    # normal methods #
    # -------------- #

    def __init__(self, view: sublime.View) -> None:
        self.view = view

    def reset(self) -> None:
        self.is_waiting = False

    def get_completion(self, index: int) -> Optional[CopilotPayloadPanelSolution]:
        return next(iter(self.completions[index : index + 1]), None)

    def append_completion(self, completion: CopilotPayloadPanelSolution) -> None:
        completions = self.completions
        completions.append(completion)
        self.completions = completions

    @staticmethod
    def find_view_by_panel_id(panel_id: str) -> Optional[sublime.View]:
        view_id = int(remove_prefix(panel_id, "copilot://"))
        return find_view_by_id(view_id)

    def open(self) -> None:
        """Open the completion panel."""
        _PanelCompletion(self.view).open()

    def update(self) -> None:
        """Update the completion panel."""
        _PanelCompletion(self.view).update()

    def close(self) -> None:
        """Close the completion panel."""
        _PanelCompletion(self.view).close()


class _PanelCompletion:
    CSS_CLASS_NAME = "copilot-completion-panel"
    CSS = """
    html {{
        --copilot-close-foreground: var(--foreground);
        --copilot-close-background: var(--background);
        --copilot-close-border: var(--redish);
        --copilot-accept-foreground: var(--foreground);
        --copilot-accept-background: var(--background);
        --copilot-accept-border: var(--greenish);
    }}

    .{class_name} {{
        margin: 1rem 0.5rem 0 0.5rem;
    }}

    .{class_name} .navbar {{
        text-align: left;
    }}

    .{class_name} .header {{
        display: block;
        margin-bottom: 1rem;
    }}

    .{class_name} a {{
        border-radius: 3px;
        border-style: solid;
        border-width: 1px;
        display: inline;
        padding: 5px;
        text-decoration: none;
    }}

    .{class_name} a.close {{
        background: var(--copilot-close-background);
        border-color: var(--copilot-close-border);
        color: var(--copilot-close-foreground);
        text-align: right;
    }}

    .{class_name} a.close i {{
        color: var(--copilot-close-border);
    }}

    .{class_name} a.accept {{
        background: var(--copilot-accept-background);
        border-color: var(--copilot-accept-border);
        color: var(--copilot-accept-foreground);
    }}

    .{class_name} a.accept i {{
        color: var(--copilot-accept-border);
    }}
    """.format(
        class_name=CSS_CLASS_NAME
    )
    COMPLETION_TEMPLATE = reformat(
        """
        <div class="navbar"><a class="close" title="Close Completion Panel" href='{close_panel}'><i>×</i> Close</a></div>
        <br>
        <div><h4>Synthesizing {index}/{total_solutions} solutions (Duplicates hidden)</h4></div>
        <hr>
        {sections}
        """
    )
    COMPLETION_SECTION_TEMPLATE = reformat(
        """
        <div class="header">{header_items}</div>
        ```{lang}
        {code}
        ```
        """
    )

    def __init__(self, view: sublime.View) -> None:
        self.view = view
        self.completion_manager = ViewPanelCompletionManager(view)

    @property
    def completion_content(self) -> str:
        completions = self._synthesize(self.completion_manager.completions)
        return self.COMPLETION_TEMPLATE.format(
            close_panel=sublime.command_url(
                    "copilot_close_panel_completion",
                    {"view_id": self.view.id()},
                ),
            index=len(self.completion_manager.completions),
            total_solutions=self.completion_manager.completion_target_count,
            sections="\n\n<hr>\n".join(
                self.COMPLETION_SECTION_TEMPLATE.format(
                    header_items=" &nbsp;".join(self.completion_header_items(completion, self.view.id(), index)),
                    score=completion["score"],
                    lang=get_view_language_id(self.view),
                    code=self._prepare_popup_code_display_text(completion["displayText"]),
                )
                for index, completion in enumerate(completions)
            ),
        )

    @staticmethod
    def completion_header_items(completion: CopilotPayloadPanelSolution, view_id: int, index: int) -> List[str]:
        return [
            """<a class="accept" href='{}'><i>✓</i> Accept</a>""".format(
                sublime.command_url(
                    "copilot_accept_panel_completion_shim",
                    {"view_id": view_id, "completion_index": index},
                )
            ),
            "<i> Mean Probability: {}</i>".format(completion["score"]),
        ]

    def open(self) -> None:
        # TODO: show this side-by-side?
        window = self.view.window()
        if not window:
            # error message
            return

        current_group = window.active_group()
        if current_group == window.num_groups() - 1:
            self._open_in_side_by_side(window)
        else:
            self._open_in_group(window, current_group + 1)

    def update(self) -> None:
        # TODO: show this side-by-side?
        window = self.view.window()
        if not window:
            # error message
            return

        sheet = find_sheet_by_group(window, self.completion_manager.group_id)
        if not sheet:
            return
            
        mdpopups_update_html_sheet(
            window=window,
            sheet=sheet,
            name="Panel Completions",
            contents=self.completion_content,
            md=True,
            css=self.CSS,
            wrapper_class=self.CSS_CLASS_NAME,
        )

    def close(self) -> None:
        # TODO: show this side-by-side?
        window = self.view.window()
        if not window:
            return

        sheet = find_sheet_by_group(window, self.completion_manager.group_id)
        if sheet is None:
            return

        sheet.close()
        if self.completion_manager.original_layout:
            window.set_layout(self.completion_manager.original_layout)
            erase_copilot_view_setting(self.view, "original_layout")

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
    def _synthesize(completions: Iterable[CopilotPayloadPanelSolution]) -> List[CopilotPayloadPanelSolution]:
        return sorted(unique(completions, itemgetter("completionText")), key=itemgetter("score"), reverse=True)

    def _open_in_group(self, window: sublime.Window, group_id: int) -> None:
        self.completion_manager.group_id = group_id

        window.focus_group(group_id)
        sheet = mdpopups.new_html_sheet(
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
        window.set_layout(
            {
                "cols": [0.0, 0.5, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
            }
        )
        self._open_in_group(window, 1)

