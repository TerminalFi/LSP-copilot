import sublime
import sublime_plugin
from .core.edit import parse_range as parse_range
from .core.logging import debug as debug
from .core.protocol import TextEdit as TextEdit, WorkspaceEdit as WorkspaceEdit
from .core.registry import LspWindowCommand as LspWindowCommand
from _typeshed import Incomplete
from typing import Any, Generator, Iterable

TextEditTuple = tuple[tuple[int, int], tuple[int, int], str]

def temporary_setting(settings: sublime.Settings, key: str, val: Any) -> Generator[None, None, None]: ...

class LspApplyWorkspaceEditCommand(LspWindowCommand):
    def run(self, session_name: str, edit: WorkspaceEdit, is_refactoring: bool = False) -> None: ...

class LspApplyDocumentEditCommand(sublime_plugin.TextCommand):
    re_placeholder: Incomplete
    def run(self, edit: sublime.Edit, changes: list[TextEdit], required_view_version: int | None = None, process_placeholders: bool = False) -> None: ...
    def apply_change(self, region: sublime.Region, replacement: str, edit: sublime.Edit) -> None: ...
    def parse_snippet(self, replacement: str) -> tuple[str, tuple[int, int]] | None: ...

def _parse_text_edit(text_edit: TextEdit) -> TextEditTuple: ...
def _sort_by_application_order(changes: Iterable[TextEditTuple]) -> list[TextEditTuple]: ...
