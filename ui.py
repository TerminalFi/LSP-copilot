import textwrap

import mdpopups
import sublime
from LSP.plugin.core.typing import List, Tuple

from .types import CopilotPayloadCompletion
from .utils import erase_copilot_view_setting, get_copilot_view_setting, reformat, set_copilot_view_setting


class Completion:
    def __init__(self, view: sublime.View) -> None:
        self.view = view

    @property
    def region(self) -> Tuple[int, int]:
        return get_copilot_view_setting(self.view, "region") or (-1, -1)

    @property
    def display_text(self) -> str:
        return get_copilot_view_setting(self.view, "display_text") or ""

    def is_visible(self) -> bool:
        return bool(self.region) and bool(self.display_text)

    def get_display_text(self, region: Tuple[int, int], raw_display_text: str) -> str:
        if "\n" in raw_display_text:
            return raw_display_text

        if self.view.classify(region[1]) & sublime.CLASS_LINE_END:
            return raw_display_text

        current_line = self.view.line(region[1])
        following_text = self.view.substr(sublime.Region(region[0], current_line.end())).strip()
        index = raw_display_text.find(following_text)

        return raw_display_text[:index] if index != -1 else raw_display_text

    def hide(self) -> None:
        PopupCompletion.hide(self.view)

        erase_copilot_view_setting(self.view, "region")
        erase_copilot_view_setting(self.view, "display_text")

    def show(self, region: Tuple[int, int], completions: List[CopilotPayloadCompletion], cycle: int = 0) -> None:
        cycle %= len(completions)
        display_text = self.get_display_text(region, completions[cycle]["displayText"])

        if not display_text:
            return

        set_copilot_view_setting(self.view, "region", region)
        set_copilot_view_setting(self.view, "display_text", display_text)

        PopupCompletion(self.view, region, display_text).show()


class PopupCompletion:
    CSS_CLASS_NAME = "copilot-suggestion-popup"
    CSS = """
    html {{
        --copilot-accept-foreground: var(--foreground);
        --copilot-accept-background: var(--background);
        --copilot-accept-border: var(--greenish);
        --copilot-dismiss-foreground: var(--foreground);
        --copilot-dismiss-background: var(--background);
        --copilot-dismiss-border: var(--yellowish);
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

    .{class_name} a.dismiss {{
        background: var(--copilot-dismiss-background);
        border-color: var(--copilot-dismiss-border);
        color: var(--copilot-dismiss-foreground);
    }}

    .{class_name} a.dismiss i {{
        color: var(--copilot-dismiss-border);
    }}
    """.format(
        class_name=CSS_CLASS_NAME
    )
    COMPLETION_TEMPLATE = reformat(
        """
        <div class="header">
            <a class="accept" href="subl:copilot_accept_suggestion"><i>✓</i> Accept</a>&nbsp;
            <a class="dismiss" href="subl:copilot_dismiss_suggestion"><i>×</i> Dismiss</a>
        </div>
        ```{lang}
        {code}
        ```
        """
    )

    def __init__(self, view: sublime.View, region: Tuple[int, int], display_text: str) -> None:
        self.view = view
        self.region = region
        self.display_text = display_text
        self.syntax = self.view.syntax() or sublime.find_syntax_by_name("Plain Text")[0]

    @property
    def content(self) -> str:
        return self.COMPLETION_TEMPLATE.format(
            lang=self.syntax.scope.rpartition(".")[2],
            code=self._prepare_display_text(),
        )

    def show(self) -> None:
        self.hide(self.view)

        mdpopups.show_popup(
            view=self.view,
            region=sublime.Region(max(self.region)),
            content=self.content,
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

    def _prepare_display_text(self) -> str:
        # The returned suggestion is in the form of
        #   - the first won't be indented
        #   - the rest of lines will be indented basing on the indentation level of the current line
        # The rest of lines don't visually look good if the current line is deeply indented.
        # Hence we modify the rest of lines into always indented by one level if it's originally indented.
        first_line, sep, rest = self.display_text.partition("\n")

        if rest.startswith("\t"):
            return first_line + sep + textwrap.indent(textwrap.dedent(rest), "\t")

        return self.display_text
