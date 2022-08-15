import html
import textwrap
from abc import ABCMeta, abstractmethod

import mdpopups
import sublime
from LSP.plugin.core.typing import Dict, List, Optional, Sequence, Type, Union

from ..types import CopilotPayloadCompletion
from ..utils import (
    clamp,
    fix_completion_syntax_highlight,
    get_copilot_view_setting,
    get_view_language_id,
    reformat,
    set_copilot_view_setting,
)

# @todo When a view is closed, it should be deleted from this dict.
_view_to_phantom_set = {}  # type: Dict[int, sublime.PhantomSet]


class _BaseCompletion(metaclass=ABCMeta):
    def __init__(
        self, view: sublime.View, completion: CopilotPayloadCompletion, index: int = 0, count: int = 1
    ) -> None:
        self.view = view
        self.completion = completion
        self.index = index
        self.count = count

        self._settings = self.view.settings()

    @abstractmethod
    def show(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def hide(cls, _: sublime.View) -> None:
        pass


class ViewCompletionManager:
    COMPLETION_STYLE_PHANTOM = "phantom"
    COMPLETION_STYLES = ["popup", COMPLETION_STYLE_PHANTOM]

    # ------------- #
    # view settings #
    # ------------- #

    @property
    def is_visible(self) -> bool:
        """Whether Copilot's completion popup is visible."""
        return get_copilot_view_setting(self.view, "is_visible", False)

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "is_visible", value)

    @property
    def is_waiting(self) -> bool:
        """Whether the view is waiting for Copilot's completion response."""
        return get_copilot_view_setting(self.view, "is_waiting_completion", False)

    @is_waiting.setter
    def is_waiting(self, value: bool) -> None:
        set_copilot_view_setting(self.view, "is_waiting_completion", value)

    @property
    def completions(self) -> List[CopilotPayloadCompletion]:
        """All `completions` in the view. Note that this is a copy."""
        return get_copilot_view_setting(self.view, "completions", [])

    @completions.setter
    def completions(self, value: List[CopilotPayloadCompletion]) -> None:
        set_copilot_view_setting(self.view, "completions", value)

    @property
    def completion_style(self) -> str:
        """The completion style."""
        return get_copilot_view_setting(self.view, "completion_style", self.COMPLETION_STYLES[0])

    @completion_style.setter
    def completion_style(self, value: str) -> None:
        set_copilot_view_setting(
            self.view,
            "completion_style",
            value if value in self.COMPLETION_STYLES else self.COMPLETION_STYLES[0],
        )

    @property
    def completion_index(self) -> int:
        """The index of the current chosen completion."""
        return get_copilot_view_setting(self.view, "completion_index", 0)

    @completion_index.setter
    def completion_index(self, value: int) -> None:
        set_copilot_view_setting(
            self.view,
            "completion_index",
            self._tidy_completion_index(value),
        )

    # -------------- #
    # normal methods #
    # -------------- #

    def __init__(self, view: sublime.View) -> None:
        self.view = view

    def reset(self) -> None:
        self.is_visible = False
        self.is_waiting = False

    @property
    def current_completion(self) -> Optional[CopilotPayloadCompletion]:
        """The current chosen `completion`."""
        return self.completions[self.completion_index] if self.completions else None

    @property
    def completion_style_type(self) -> Type[_BaseCompletion]:
        return globals().get("_{}Completion".format(self.completion_style.capitalize()))

    def is_phantom(self) -> bool:
        return self.completion_style == self.COMPLETION_STYLE_PHANTOM

    def show_previous_completion(self) -> None:
        """Show the previous completion."""
        self.show(completion_index=self.completion_index - 1)

    def show_next_completion(self) -> None:
        """Show the next completion."""
        self.show(completion_index=self.completion_index + 1)

    def handle_selection_change(self) -> None:
        if not self.is_phantom():
            return

        self.completion_style_type.hide(self.view)

    def hide(self) -> None:
        """Hide Copilot's completion popup."""
        # prevent from hiding other plugin's popup
        if self.is_visible:
            _PopupCompletion.hide(self.view)
            _PhantomCompletion.hide(self.view)

        self.is_visible = False

    def show(
        self,
        completions: Optional[List[CopilotPayloadCompletion]] = None,
        completion_index: Optional[int] = None,
        completion_style: Optional[str] = None,
    ) -> None:
        """Show Copilot's completion popup."""
        if completions is not None:
            self.completions = completions
        if completion_index is not None:
            self.completion_index = completion_index
        if completion_style is not None:
            self.completion_style = completion_style

        completion = self.current_completion
        if not completion:
            return

        # the text after completion is the same
        current_line = self.view.line(completion["point"])
        if completion["text"] == self.view.substr(current_line):
            return

        self.completion_style_type(
            self.view, self.current_completion, self.completion_index, len(self.completions)
        ).show()

        self.is_visible = True

    def _tidy_completion_index(self, index: int) -> int:
        """Revise `completion_index` to a valid value, or `0` if `self.completions` is empty."""
        completions_cnt = len(self.completions)
        if not completions_cnt:
            return 0

        # clamp if it's out-of-bounds or treat it as cyclic?
        if self.view.settings().get("auto_complete_cycle"):
            return index % completions_cnt
        return clamp(index, 0, completions_cnt - 1)


class _PopupCompletion(_BaseCompletion):
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

    .{class_name} a.panel {{
        padding-left: 8px;
        padding-right: 8px;
    }}
    """.format(
        class_name=CSS_CLASS_NAME
    )
    # We use many backticks to denote a fenced code block because if we are writing in Markdown,
    # Copilot may suggest 3 backticks for a fenced code block and that can break our templating.
    COMPLETION_TEMPLATE = reformat(
        """
        <div class="header">{header_items}</div>
        ``````{lang}
        {code}
        ``````
        """
    )

    @property
    def popup_content(self) -> str:
        return self.COMPLETION_TEMPLATE.format(
            header_items=" &nbsp;".join(self.popup_header_items),
            lang=get_view_language_id(self.view, self.completion["point"]),
            code=self.popup_code,
        )

    @property
    def popup_header_items(self) -> List[str]:
        header_items = [
            '<a class="accept" title="Accept Completion" href="subl:copilot_accept_completion"><i>✓</i> Accept</a>',
            '<a class="reject" title="Reject Completion" href="subl:copilot_reject_completion"><i>×</i> Reject</a>',
        ]
        if self.count > 1:
            header_items.append(
                '<a class="prev" title="Previous Completion" href="subl:copilot_previous_completion">◀</a>'
                + '<a class="next" title="Next Completion" href="subl:copilot_next_completion">▶</a>'
            )
            header_items.append(
                "({completion_index_1} of {completions_cnt})".format(
                    completion_index_1=self.index + 1,  # 1-based index
                    completions_cnt=self.count,
                )
            )
        header_items.append(
            '<a class="panel" href="subl:copilot_get_panel_completions" title="Open Panel Completions">☰</a>'
        )
        return header_items

    @property
    def popup_code(self) -> str:
        return fix_completion_syntax_highlight(
            self.view,
            self.completion["point"],
            textwrap.dedent(self.completion["text"]),
        )

    def show(self) -> None:
        mdpopups.show_popup(
            view=self.view,
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


class _PhantomCompletion(_BaseCompletion):
    COPILOT_PHANTOM_COMPLETION = "copilot_phantom_completion"
    PHANTOM_TEMPLATE = """
    <body id="copilot-completion">
        <style>
            body {{
                color: #808080;
                font-style: italic;
            }}

            .copilot-completion-line {{
                margin-top: {line_padding_top}px;
                margin-bottom: {line_padding_bottom}px;
            }}

            .copilot-completion-line.first {{
                margin-top: 0;
            }}
        </style>
        {body}
    </body>
    """
    PHANTOM_LINE_TEMPLATE = '<div class="copilot-completion-line {class_name}">{content}</div>'

    def __init__(
        self, view: sublime.View, completion: CopilotPayloadCompletion, index: int = 0, count: int = 1
    ) -> None:
        super().__init__(view, completion, index, count)

        self._phantom_set = self._get_phantom_set(view)

    @classmethod
    def _get_phantom_set(cls, view: sublime.View) -> sublime.PhantomSet:
        view_id = view.id()

        # create phantom set if there is no existing one
        if not _view_to_phantom_set.get(view_id):
            _view_to_phantom_set[view_id] = sublime.PhantomSet(view, cls.COPILOT_PHANTOM_COMPLETION)

        return _view_to_phantom_set[view_id]

    def normalize_phantom_line(self, line: str) -> str:
        return html.escape(line).replace(" ", "&nbsp;").replace("\t", "&nbsp;" * self._settings.get("tab_size"))

    def _build_phantom(
        self,
        lines: Union[str, Sequence[str]],
        begin: int,
        end: Optional[int] = None,
        *,
        inline: bool = True
        # format separator
    ) -> sublime.Phantom:
        body = (
            self.normalize_phantom_line(lines)
            if isinstance(lines, str)
            else "".join(
                self.PHANTOM_LINE_TEMPLATE.format(
                    class_name=("rest" if index else "first"),
                    content=self.normalize_phantom_line(line),
                )
                for index, line in enumerate(lines)
            )
        )

        return sublime.Phantom(
            sublime.Region(begin, begin if end is None else end),
            self.PHANTOM_TEMPLATE.format(
                body=body,
                line_padding_top=int(self._settings.get("line_padding_top")) * 2,  # TODO: play with this more
                line_padding_bottom=int(self._settings.get("line_padding_bottom")) * 2,
            ),
            sublime.LAYOUT_INLINE if inline else sublime.LAYOUT_BLOCK,
        )

    def show(self) -> None:
        first_line, *rest_lines = self.completion["displayText"].splitlines()

        assert self._phantom_set
        self._phantom_set.update([])
        self._phantom_set.update(
            [
                self._build_phantom(first_line, self.completion["point"] + 1, self.completion["point"]),
                # an empty phantom is required to prevent the cursor from jumping, even if there is only one line
                self._build_phantom(rest_lines, self.completion["point"], inline=False),
            ]
        )

    @classmethod
    def hide(cls, view: sublime.View) -> None:
        cls._get_phantom_set(view).update([])
