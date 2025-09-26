from _typeshed import Incomplete
from typing import Generator
from unittesting import DeferrableTestCase

class WindowDocumentHandlerTests(DeferrableTestCase):
    def ensure_document_listener_created(self) -> bool: ...
    window: Incomplete
    session1: Incomplete
    session2: Incomplete
    config1: Incomplete
    config2: Incomplete
    wm: Incomplete
    def setUp(self) -> Generator: ...
    view: Incomplete
    def test_sends_did_open_to_multiple_sessions(self) -> Generator: ...
    def doCleanups(self) -> Generator: ...
    def await_message(self, method: str) -> Generator: ...
