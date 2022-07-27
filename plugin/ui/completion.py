import textwrap
from abc import ABCMeta, abstractmethod
from functools import partial

import mdpopups
import sublime
from LSP.plugin.core.typing import List, Optional

from ..types import CopilotPayloadCompletion
from ..utils import clamp, get_copilot_view_setting, get_view_language_id, reformat, set_copilot_view_setting


class ViewCompletionManager:
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

    def show_previous_completion(self) -> None:
        """Show the previous completion."""
        self.show(completion_index=self.completion_index - 1)

    def show_next_completion(self) -> None:
        """Show the next completion."""
        self.show(completion_index=self.completion_index + 1)

    def handle_selection_change(self) -> None:
        _PhantomCompletion.hide(self.view)

    def hide(self) -> None:
        """Hide Copilot's completion popup."""
        # prevent from hiding other plugin's popup
        if self.is_visible:
            _PopupCompletion.hide(self.view)
            _PhantomCompletion.hide(self.view)

    def show(
        self,
        completions: Optional[List[CopilotPayloadCompletion]] = None,
        completion_index: Optional[int] = None,
    ) -> None:
        """Show Copilot's completion popup."""
        if completions is not None:
            self.completions = completions
        if completion_index is not None:
            self.completion_index = completion_index

        completion = self.current_completion
        if not completion:
            return

        # the text after completion is the same
        current_line = self.view.line(completion["point"])
        if completion["text"] == self.view.substr(current_line):
            return

        _PopupCompletion(self.view).show()
        _PhantomCompletion(self.view).show()

    def _tidy_completion_index(self, index: int) -> int:
        """Revise `completion_index` to a valid value, or `0` if `self.completions` is empty."""
        completions_cnt = len(self.completions)
        if not completions_cnt:
            return 0

        # clamp if it's out-of-bounds or treat it as cyclic?
        if self.view.settings().get("auto_complete_cycle", False):
            return index % completions_cnt
        return clamp(index, 0, completions_cnt - 1)


class _BaseCompletion(metaclass=ABCMeta):
    def __init__(self, view: sublime.View) -> None:
        self.view = view
        self.completion_manager = ViewCompletionManager(view)

    @abstractmethod
    def show(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def hide(cls, _: sublime.View) -> None:
        pass


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
    COMPLETION_TEMPLATE = reformat(
        """
        <div class="header">{header_items}</div>
        ```{lang}
        {code}
        ```
        """
    )

    @property
    def popup_content(self) -> str:
        return self.COMPLETION_TEMPLATE.format(
            header_items=" &nbsp;".join(self.popup_header_items),
            lang=get_view_language_id(self.view),
            code=self.popup_code,
        )

    @property
    def popup_header_items(self) -> List[str]:
        completions_cnt = len(self.completion_manager.completions)
        header_items = [
            '<a class="accept" title="Accept Completion" href="subl:copilot_accept_completion"><i>✓</i> Accept</a>',
            '<a class="reject" title="Reject Completion" href="subl:copilot_reject_completion"><i>×</i> Reject</a>',
        ]
        if completions_cnt > 1:
            header_items.append(
                '<a class="prev" title="Previous Completion" href="subl:copilot_previous_completion">◀</a>'
                + '<a class="next" title="Next Completion" href="subl:copilot_next_completion">▶</a>'
            )
            header_items.append(
                "({completion_index_1} of {completions_cnt})".format(
                    completion_index_1=self.completion_manager.completion_index + 1,  # 1-based index
                    completions_cnt=completions_cnt,
                )
            )
        header_items.append(
            '<a class="panel" href="subl:copilot_get_panel_completions" title="Open Panel Completions">☰</a>'
        )
        return header_items

    @property
    def popup_code(self) -> str:
        self.completion = self.completion_manager.current_completion
        assert self.completion  # our code flow guarantees this
        return textwrap.dedent(self.completion["text"])

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
            on_hide=partial(set_copilot_view_setting, self.view, "is_visible", False),
        )
        # It's tricky that the "on_hide" is async...
        sublime.set_timeout_async(partial(set_copilot_view_setting, self.view, "is_visible", True))

    @staticmethod
    def hide(view: sublime.View) -> None:
        mdpopups.hide_popup(view)


_phantom_sets_per_view = {}


class _PhantomCompletion(_BaseCompletion):
    COPILOT_PHANTOM_COMPLETION = "copilot_phantom_completion"
    PHANTOM_TEMPLATE = """
    <body id="copilot-completion">
        <style>
            body {{
                color: #808080;
            }}
        </style>
        {body}
    </body>
    """

    def __init__(self, view: sublime.View) -> None:
        super().__init__(view)

        self._phantom_set = self._get_phantom_set(view, True)

    @classmethod
    def _get_phantom_set(cls, view: sublime.View, init: bool = False) -> Optional[sublime.PhantomSet]:
        view_id = view.id()
        phantom_set = _phantom_sets_per_view.get(view_id, None)

        if init:
            phantom_set = sublime.PhantomSet(view, cls.COPILOT_PHANTOM_COMPLETION)
            _phantom_sets_per_view[view_id] = phantom_set

        return phantom_set

    # def _build_phantom(self, content: str) -> sublime.Phantom:
    #     return sublime.Phantom(
    #         sublime.Region(self.region[0] + 1, self.region[1]),
    #         self.PHANTOM_TEMPLATE.format(body=content),
    #         sublime.LAYOUT_INLINE,
    #     )

    def show(self) -> None:
        phantoms = []
        completion = self.completion_manager.current_completion
        assert completion
        head, *tail = completion["displayText"].split("\n")

        phantoms.append(
            sublime.Phantom(
                sublime.Region(completion["point"] + 1, completion["point"]),
                self.PHANTOM_TEMPLATE.format(body=head),
                sublime.LAYOUT_INLINE,
            )
        )

        # if bool(tail):
        #     pass
        # else:
        # it is required to add an empty phantom to prevent the cursor from jumping
        phantoms.append(
            sublime.Phantom(
                sublime.Region(completion["point"], completion["point"]),
                "",
                sublime.LAYOUT_BLOCK,
            )
        )

        self._phantom_set.update(phantoms)

    @classmethod
    def hide(cls, view: sublime.View) -> None:
        phantom_set = cls._get_phantom_set(view)

        if phantom_set:
            phantom_set.update([])
