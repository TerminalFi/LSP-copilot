import textwrap

import mdpopups
import sublime
from LSP.plugin.core.typing import List, Tuple

from .constants import COPILOT_VIEW_SETTINGS_PREFIX
from .types import CopilotPayloadCompletion


class Completion:
    def __init__(self, view: sublime.View):
        self.view = view

    def _settings(self, key, default_or_new_value=None, do: str = "get"):
        settings_key = "{}.{}".format(COPILOT_VIEW_SETTINGS_PREFIX, key)

        if do == "set":
            return self.view.settings().set(settings_key, default_or_new_value)
        elif do == "erase":
            return self.view.settings().erase(settings_key)
        else:
            return self.view.settings().get(settings_key, default_or_new_value)

    @property
    def region(self):
        return self._settings("region")

    @property
    def display_text(self):
        return self._settings("display_text")

    @property
    def uuid(self):
        return self._settings("uuid")

    def is_visible(self) -> bool:
        return bool(self.region) and bool(self.display_text)

    def get_display_text(self, region: Tuple[int, int], raw_display_text: str):
        if "\n" in raw_display_text:
            return raw_display_text

        if (self.view.classify(region[1]) & sublime.CLASS_LINE_END) != 0:
            return raw_display_text

        current_line = self.view.line(region[1])
        following_text = self.view.substr(sublime.Region(region[0], current_line.end())).strip()
        index = raw_display_text.find(following_text)

        return raw_display_text[:index] if index != -1 else raw_display_text

    def hide(self):
        PopupCompletion.hide(self.view)

        self._settings("region", do="erase")
        self._settings("display_text", do="erase")

    def show(self, region: Tuple[int, int], completions: List[CopilotPayloadCompletion], cycle: int = 0):
        cycle %= len(completions)

        completion_uuid = completions[cycle]["uuid"]

        display_text = self.get_display_text(region, completions[cycle]["displayText"])
        if not display_text:
            return


        self._settings("region", region, do="set")
        self._settings("uuid", completion_uuid, do="set")
        self._settings("display_text", display_text, do="set")

        PopupCompletion(self.view, region, display_text).show()


class PopupCompletion:
    CSS_CLASS_NAME = "copilot-suggestion-popup"
    CSS = """
    .{class_name} {{
        margin-left: 10px;
        margin-right: 10px;
        margin-top: 10px;
    }}

    .{class_name} a {{
        display: block;
    }}
    """.format(
        class_name=CSS_CLASS_NAME
    )
    COMPLETION_TEMPLATE = '<a href="subl:copilot_accept_suggestion">Accept ⇥</a>\n```{lang}\n{code}\n```'

    @staticmethod
    def hide(view: sublime.View):
        mdpopups.hide_popup(view)

    def __init__(self, view: sublime.View, region: Tuple[int, int], display_text: str):
        self.view = view
        self.region = region
        self.display_text = display_text

        self.syntax = self.view.syntax()

    def _prepare_display_text(self):
        # The returned suggestion is in the form of
        #   - the first won't be indented
        #   - the rest of lines will be indented basing on the indentation level of the current line
        # The rest of lines don't visually look good if the current line is deeply indented.
        # Hence we modify the rest of lines into always indented by one level if it's originally indented.
        first_line, sep, rest = self.display_text.partition("\n")

        if rest.startswith("\t"):
            return first_line + sep + textwrap.indent(textwrap.dedent(rest), "\t")

        return self.display_text

    @property
    def content(self):
        return self.COMPLETION_TEMPLATE.format(
            lang=self.syntax.scope.rpartition(".")[2],
            code=self._prepare_display_text(),
        )

    def show(self) -> bool:
        self.hide(self.view)

        if not self.syntax:
            return False

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

        return True
