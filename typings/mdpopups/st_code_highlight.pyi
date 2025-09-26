from .st_mapping import lang_map as lang_map
from _typeshed import Incomplete

RE_TAIL: Incomplete
INLINE_BODY_START: str
BODY_START: str
LINE: str
INLINE_LINE: str
CODE: str
CODEBG: str
BODY_END: str
INLINE_BODY_END: str
ST_LANGUAGES: Incomplete

class SublimeHighlight:
    view: Incomplete
    def __init__(self, scheme) -> None: ...
    tab_size: int
    size: Incomplete
    pt: int
    end: int
    curr_row: int
    def setup(self, **kwargs) -> None: ...
    start_line: Incomplete
    def setup_print_block(self, curr_sel, multi: bool = False) -> None: ...
    def print_line(self, line, num): ...
    char_count: int
    def convert_view_to_html(self) -> None: ...
    def html_encode(self, text): ...
    def format_text(self, line, text, color, bgcolor, style, empty, annotate: bool = False) -> None: ...
    def convert_line_to_html(self, empty): ...
    def write_body(self) -> None: ...
    def set_view(self, src, lang, plugin_map) -> None: ...
    defaults: Incomplete
    fground: Incomplete
    bground: Incomplete
    inline: Incomplete
    hl_lines: Incomplete
    no_wrap: Incomplete
    code_wrap: Incomplete
    html: Incomplete
    def syntax_highlight(self, src, lang, hl_lines=[], inline: bool = False, no_wrap: bool = False, code_wrap: bool = False, plugin_map: Incomplete | None = None): ...
    def set_syntax_by_scope(self, scope): ...
