from _typeshed import Incomplete

class CSS:
    popups: Incomplete
    popups_classname: str
    notification: Incomplete
    notification_classname: str
    sheets: Incomplete
    sheets_classname: str
    inlay_hints: Incomplete
    annotations: Incomplete
    annotations_classname: str
    def __init__(self) -> None: ...

_css: CSS | None

def load() -> None: ...
def css() -> CSS: ...
