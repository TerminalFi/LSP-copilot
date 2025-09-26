import sublime
from .core.protocol import Location as Location, LocationLink as LocationLink, Request as Request
from .core.registry import LspTextCommand as LspTextCommand, get_position as get_position
from .core.sessions import Session as Session, method_to_capability as method_to_capability
from .core.views import get_symbol_kind_from_scope as get_symbol_kind_from_scope, text_document_position_params as text_document_position_params
from .locationpicker import LocationPicker as LocationPicker, open_location_async as open_location_async
from _typeshed import Incomplete

class LspGotoCommand(LspTextCommand):
    method: str
    placeholder_text: str
    fallback_command: str
    def is_enabled(self, event: dict | None = None, point: int | None = None, side_by_side: bool = False, force_group: bool = True, fallback: bool = False, group: int = -1) -> bool: ...
    def is_visible(self, event: dict | None = None, point: int | None = None, side_by_side: bool = False, force_group: bool = True, fallback: bool = False, group: int = -1) -> bool: ...
    def run(self, _: sublime.Edit, event: dict | None = None, point: int | None = None, side_by_side: bool = False, force_group: bool = True, fallback: bool = False, group: int = -1) -> None: ...
    def _handle_response_async(self, session: Session, side_by_side: bool, force_group: bool, fallback: bool, group: int, position: int, response: None | Location | list[Location] | list[LocationLink]) -> None: ...
    def _handle_no_results(self, fallback: bool = False, side_by_side: bool = False) -> None: ...

class LspSymbolDefinitionCommand(LspGotoCommand):
    method: str
    capability: Incomplete
    placeholder_text: str
    fallback_command: str

class LspSymbolTypeDefinitionCommand(LspGotoCommand):
    method: str
    capability: Incomplete
    placeholder_text: str

class LspSymbolDeclarationCommand(LspGotoCommand):
    method: str
    capability: Incomplete
    placeholder_text: str

class LspSymbolImplementationCommand(LspGotoCommand):
    method: str
    capability: Incomplete
    placeholder_text: str
