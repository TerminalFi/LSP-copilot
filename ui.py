import textwrap
from functools import partial

import mdpopups
import sublime
from LSP.plugin.core.types import basescope2languageid
from LSP.plugin.core.typing import List, Optional

from .types import CopilotPayloadCompletion, CopilotPayloadPanelSolution
from .utils import clamp, first, get_copilot_view_setting, reformat, set_copilot_view_setting


class ViewCompletionManager:
    def __init__(self, view: sublime.View) -> None:
        self.view = view

    @property
    def is_visible(self) -> bool:
        """Whether Copilot's completion popup is visible."""
        return get_copilot_view_setting(self.view, "is_visible", False)

    @property
    def panel_completions(self) -> List[CopilotPayloadPanelSolution]:
        """All `panel_completions` in the view."""
        return get_copilot_view_setting(self.view, "panel_completions", [])

    @property
    def completions(self) -> List[CopilotPayloadCompletion]:
        """All `completions` in the view."""
        return get_copilot_view_setting(self.view, "completions", [])

    @property
    def completion_index(self) -> int:
        """The index of the current chosen completion."""
        return get_copilot_view_setting(self.view, "completion_index", 0)

    @property
    def current_completion(self) -> Optional[CopilotPayloadCompletion]:
        """The current chosen `completion`."""
        return self.completions[self.completion_index] if self.completions else None

    def get_panel_completion(self, index: int) -> Optional[CopilotPayloadPanelSolution]:
        """The chosen `solution`."""
        return self.panel_completions[index] if len(self.panel_completions) >= index else None

    def show_previous_completion(self) -> None:
        """Show the previous completion."""
        self.show(
            completion_index=self.completion_index - 1,
            do_clamp=not self.view.settings().get("auto_complete_cycle", False),
        )

    def show_next_completion(self) -> None:
        """Show the next completion."""
        self.show(
            completion_index=self.completion_index + 1,
            do_clamp=not self.view.settings().get("auto_complete_cycle", False),
        )

    def hide(self) -> None:
        """Hide Copilot's completion popup."""
        # prevent from hiding other plugin's popup
        if self.is_visible:
            _PopupCompletion.hide(self.view)

    def show(
        self,
        completions: Optional[List[CopilotPayloadCompletion]] = None,
        completion_index: Optional[int] = None,
        do_clamp: bool = True,
    ) -> None:
        """Show Copilot's completion popup."""
        # update completions
        if completions is not None:
            set_copilot_view_setting(self.view, "completions", completions)
        # update completion index
        if completion_index is not None:
            set_copilot_view_setting(self.view, "completion_index", completion_index)
        self._tidy_completion_index(do_clamp)

        completion = self.current_completion
        if not completion:
            return

        # the text after completion is the same
        current_line = self.view.line(completion["positionSt"])
        if completion["text"] == self.view.substr(current_line):
            return

        _PopupCompletion(self.view).show()

    def open_panel_completions(self) -> None:
        """Open panel completions."""
        _PanelCompletion(self.view).open()

    def update_panel_completions(self) -> None:
        """Open panel completions."""
        _PanelCompletion(self.view).update()

    def _tidy_completion_index(self, do_clamp: bool = True) -> None:
        """
        Revise `completion_index` to a valid value, or `0` if `self.completions` is empty.

        :param      do_clamp:  Clamp `completion_index` if it's out-of-bounds. Otherwise, treat it as cyclic.
        """
        completions_cnt = len(self.completions)
        if completions_cnt:
            if do_clamp:
                new_index = clamp(self.completion_index, 0, completions_cnt - 1)
            else:
                new_index = self.completion_index % completions_cnt
        else:
            new_index = 0
        set_copilot_view_setting(self.view, "completion_index", new_index)


class _PopupCompletion:
    CSS_CLASS_NAME = "copilot-completion-popup"
    CSS = """
    html {{
        --copilot-accept-foreground: var(--foreground);
        --copilot-accept-background: var(--background);
        --copilot-accept-border: var(--greenish);
        --copilot-reject-foreground: var(--foreground);
        --copilot-reject-background: var(--background);
        --copilot-reject-border: var(--yellowish);
    }}

    .{class_name} {{
        margin: 1rem 0.5rem 0 0.5rem;
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

    .{class_name} a.accept {{
        background: var(--copilot-accept-background);
        border-color: var(--copilot-accept-border);
        color: var(--copilot-accept-foreground);
    }}

    .{class_name} a.accept i {{
        color: var(--copilot-accept-border);
    }}

    .{class_name} a.reject {{
        background: var(--copilot-reject-background);
        border-color: var(--copilot-reject-border);
        color: var(--copilot-reject-foreground);
    }}

    .{class_name} a.reject i {{
        color: var(--copilot-reject-border);
    }}

    .{class_name} a.prev {{
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;
        border-right-width: 0;
        padding-left: 8px;
        padding-right: 8px;
    }}

    .{class_name} a.next {{
        border-top-left-radius: 0;
        border-bottom-left-radius: 0;
        border-left-width: 0;
        padding-left: 8px;
        padding-right: 8px;
    }}
    """.format(
        class_name=CSS_CLASS_NAME
    )
    COMPLETION_TEMPLATE = reformat(
        """
        <div class="header">{header_items}</div>
        ```{lang}
        {code}
        ```
        """
    )

    def __init__(self, view: sublime.View) -> None:
        self.view = view
        self.completion_manager = ViewCompletionManager(view)

    @property
    def popup_content(self) -> str:
        syntax = self.view.syntax() or sublime.find_syntax_by_name("Plain Text")[0]
        return self.COMPLETION_TEMPLATE.format(
            header_items=" &nbsp;".join(self.popup_header_items),
            lang=basescope2languageid(syntax.scope),
            code=self.popup_code,
        )

    @property
    def popup_header_items(self) -> List[str]:
        completions_cnt = len(self.completion_manager.completions)
        header_items = [
            '<a class="accept" href="subl:copilot_accept_completion"><i>✓</i> Accept</a>',
            '<a class="reject" href="subl:copilot_reject_completion"><i>×</i> Reject</a>',
        ]
        if completions_cnt > 1:
            header_items.append(
                '<a class="prev" href="subl:copilot_previous_completion">◀</a>'
                + '<a class="next" href="subl:copilot_next_completion">▶</a>'
            )
            header_items.append(
                "({completion_index_1} of {completions_cnt})".format(
                    completion_index_1=self.completion_manager.completion_index + 1,  # 1-based index
                    completions_cnt=completions_cnt,
                )
            )
        return header_items

    @property
    def popup_code(self) -> str:
        self.completion = self.completion_manager.current_completion
        assert self.completion  # our code flow guarantees this
        return textwrap.dedent(self.completion["text"])

    def show(self) -> None:
        set_copilot_view_setting(self.view, "is_visible", True)
        mdpopups.show_popup(
            view=self.view,
            content=self.popup_content,
            md=True,
            css=self.CSS,
            layout=sublime.LAYOUT_INLINE,
            flags=sublime.COOPERATE_WITH_AUTO_COMPLETE,
            max_width=640,
            wrapper_class=self.CSS_CLASS_NAME,
            on_hide=partial(set_copilot_view_setting, self.view, "is_visible", False),
        )

    @staticmethod
    def hide(view: sublime.View) -> None:
        mdpopups.hide_popup(view)


class _PanelCompletion:
    CSS_CLASS_NAME = "copilot-completion-panel"
    CSS = """
    html {{
        --copilot-accept-foreground: var(--foreground);
        --copilot-accept-background: var(--background);
        --copilot-accept-border: var(--greenish);
    }}

    .{class_name} {{
        margin: 1rem 0.5rem 0 0.5rem;
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
        <h4>Synthesizing {index}/{total_solutions} solutions (Duplicates hidden)</h4>
        <hr>
        <div>Mean Probability: {score}</div>
        <div class="header">{header_items}</div>
        ```{lang}
        {code}
        ```
        """
    )

    def __init__(self, view: sublime.View) -> None:
        self.view = view
        self.completion_manager = ViewCompletionManager(view)

    @property
    def completion_content(self) -> str:
        syntax = self.view.syntax() or sublime.find_syntax_by_name("Plain Text")[0]
        return "\n\n<hr>\n".join(
            self.COMPLETION_TEMPLATE.format(
                index=len(self.completion_manager.panel_completions),
                total_solutions=get_copilot_view_setting(self.view, "panel_completion_target_count", 0),
                header_items="{}".format(
                    self.completion_header_item(self.completion_manager.panel_completions.index(item))
                ),
                score=item["score"],
                lang=basescope2languageid(syntax.scope),
                code=self._prepare_popup_code_display_text(item["displayText"]),
            )
            for item in self.completion_manager.panel_completions
        )

    @staticmethod
    def completion_header_item(index: int) -> str:
        # TODO Accept Completion Completiond ID
        return '<a class="accept" title="Accept Completion" href=\'subl:copilot_accept_panel_completion {{"index": {index}}}\'><i>✓</i> Accept</a>'.format(
            index=index
        )

    def open(self) -> None:
        # TODO: show this side-by-side?
        sheet = mdpopups.new_html_sheet(
            window=self.view.window(),
            name="Panel Completions",
            contents=self.completion_content,
            md=True,
            css=self.CSS,
            wrapper_class=self.CSS_CLASS_NAME,
        )

        set_copilot_view_setting(self.view, "panel_sheet_id", sheet.id())

    def update(self) -> None:
        # TODO: show this side-by-side?
        sheet_id = get_copilot_view_setting(self.view, "panel_sheet_id")
        if not sheet_id:
            return

        window = self.view.window()
        if not window:
            return

        target_sheet = first(window.sheets(), lambda sheet: sheet.id() == sheet_id)
        if target_sheet is None:
            return

        mdpopups.update_html_sheet(
            sheet=target_sheet,
            name="Panel Completions",
            contents=self.completion_content,
            md=True,
            css=self.CSS,
            wrapper_class=self.CSS_CLASS_NAME,
        )

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
