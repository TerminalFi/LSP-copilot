from LSP.plugin.core.protocol import PublishDiagnosticsParams as PublishDiagnosticsParams
from setup import TextDocumentTestCase
from typing import Generator

class ServerNotifications(TextDocumentTestCase):
    def test_publish_diagnostics(self) -> Generator: ...
