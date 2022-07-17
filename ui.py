import textwrap

import mdpopups
import sublime
from LSP.plugin.core.typing import List, Optional

from .types import CopilotPayloadCompletion
from .utils import clamp, get_copilot_view_setting, reformat, set_copilot_view_setting


class ViewCompletionManager:
    def __init__(self, view: sublime.View) -> None:
        self.view = view

    @property
    def is_visible(self) -> bool:
        """Whether Copilot's completion popup is visible."""
        return get_copilot_view_setting(self.view, "is_visible", False)

    @property
    def completions(self) -> List[CopilotPayloadCompletion]:
        """All `completions` in the view."""
        return get_copilot_view_setting(self.view, "completions", [])

    @property
    def completion_index(self) -> int:
        """The current index of the chosen completion."""
        return get_copilot_view_setting(self.view, "completion_index", 0)

    @property
    def current_completion(self) -> Optional[CopilotPayloadCompletion]:
        """The current chosen `completion`."""
        completions = self.completions
        return completions[self.completion_index] if completions else None

    def choose_previous_completion(self) -> None:
        """Set `completion_index` to be for the previous completion."""
        self._set_completion_index(
            self.completion_index - 1,
            do_clamp=not self.view.settings().get("auto_complete_cycle", False),
        )

    def choose_next_completion(self) -> None:
        """Set `completion_index` to be for the next completion."""
        self._set_completion_index(
            self.completion_index + 1,
            do_clamp=not self.view.settings().get("auto_complete_cycle", False),
        )

    def hide(self) -> None:
        """Hide Copilot's completion popup."""
        # to prevent from hiding other plugin's popup
        if self.is_visible:
            set_copilot_view_setting(self.view, "is_visible", False)
            _PopupCompletion.hide(self.view)

    def show(self) -> None:
        """Show Copilot's completion popup."""
        completion = self.current_completion
        if not completion:
            return

        # the text after completion is the same
        current_line = self.view.line(completion["positionSt"])
        if completion["text"] == self.view.substr(current_line):
            return

        set_copilot_view_setting(self.view, "is_visible", True)
        _PopupCompletion(self.view).show()

    def _set_completion_index(self, value: int, do_clamp: bool = False) -> None:
        """
        Set `completion_index`.

        :param      value:     The wanted new completion index.
        :param      do_clamp:  Should the `value` be clamped if it's
                               out-of-bound? Otherwise, treat it as circular.
        """
        completions_cnt = len(self.completions)
        if completions_cnt:
            value = clamp(value, 0, completions_cnt - 1) if do_clamp else value % completions_cnt
        else:
            value = 0
        set_copilot_view_setting(self.view, "completion_index", value)


class _PopupCompletion:
    CSS_CLASS_NAME = "copilot-suggestion-popup"
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
            lang=syntax.scope.rpartition(".")[2],
            code=self.popup_code,
        )

    @property
    def popup_header_items(self) -> List[str]:
        completions_cnt = len(self.completion_manager.completions)
        header_items = [
            '<a class="accept" href="subl:copilot_accept_suggestion"><i>✓</i> Accept</a>',
            '<a class="reject" href="subl:copilot_reject_suggestion"><i>×</i> Reject</a>',
        ]
        if completions_cnt > 1:
            header_items.append('<a class="previous" href="subl:copilot_previous_suggestion">▲ Previous</a>')
            header_items.append('<a class="next" href="subl:copilot_next_suggestion">▼ Next</a>')
            header_items.append(
                "({completion_index_1} of {completions_cnt})".format(
                    completion_index_1=self.completion_manager.completion_index + 1,  # 1-base index
                    completions_cnt=completions_cnt,
                )
            )
        return header_items

    @property
    def popup_code(self) -> str:
        self.completion = self.completion_manager.current_completion
        assert self.completion  # out code flow guarantees this

        display_text = self.completion["displayText"]
        position_st = self.completion["positionSt"]

        # multiple lines are not supported
        if ("\n" in display_text) or (self.view.classify(position_st) & sublime.CLASS_LINE_END):
            return self._prepare_popup_code_display_text(display_text)

        # inline completion
        current_line = self.view.line(position_st)
        following_text = self.view.substr(sublime.Region(position_st, current_line.end())).strip()
        index = display_text.find(following_text)
        return display_text[:index] if following_text and index != -1 else display_text

    def show(self) -> None:
        self.hide(self.view)

        mdpopups.show_popup(
            view=self.view,
            # multiple lines are not supported
            content=self.popup_content,
            md=True,
            css=self.CSS,
            layout=sublime.LAYOUT_INLINE,
            flags=sublime.COOPERATE_WITH_AUTO_COMPLETE,
            max_width=640,
            wrapper_class=self.CSS_CLASS_NAME,
        )

    @staticmethod
    def hide(view: sublime.View) -> None:
        mdpopups.hide_popup(view)

    @staticmethod
    def _prepare_popup_code_display_text(display_text: str) -> str:
        # The returned suggestion is in the form of
        #   - the first won't be indented
        #   - the rest of lines will be indented basing on the indentation level of the current line
        # The rest of lines don't visually look good if the current line is deeply indented.
        # Hence we modify the rest of lines into always indented by one level if it's originally indented.
        first_line, sep, rest = display_text.partition("\n")

        if rest.startswith((" ", "\t")):
            return first_line + sep + textwrap.indent(textwrap.dedent(rest), "\t")

        return display_text
