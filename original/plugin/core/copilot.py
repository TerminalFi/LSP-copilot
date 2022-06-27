
from subprocess import call
import sublime
from .handler import Handler
from .rpc import create_transport
from .constants import PLUGIN_NAME
from .constants import PLUGIN_VERSION
from .constants import COPILOT_VERION
from .constants import SUBLIME_VERSION
from .types import GET_COMPLETIONS, SIGN_OUT
from .types import INITIALIZE
from .types import SIGN_IN_CONFIRM
from .types import NOTIFY_REJECTED
from .types import NOTIFY_SHOWN
from .types import NOTIFY_ACCEPTED
from .types import SET_EDITOR_INFO
from .types import CHECK_STATUS
from .types import SIGN_IN_INITIATE
from .types import TransportConfig
from .typing import List


class Copilot:
    def __init__(self) -> None:
        self.handler = Handler()
        self.transport = None
        self._enabled = False
        self.signed_in = False
        self.current_completions = []
        self.completion_index = 0
        self.plugin_name = PLUGIN_NAME
        self.plugin_version = PLUGIN_VERSION
        self.copilot_version = COPILOT_VERION
        self.sublime_version = SUBLIME_VERSION

    def start_copilot(self) -> bool:
        if self.transport is not None:
            return False

        self.transport = create_transport(config=TransportConfig(name='Copilot', command=[
            'node', '/Users/zacharyschulze/git/Alfred-Man/copilot.el/dist/agent.js'], env={}, listener_socket=None), cwd=None, callback_object=self.handler)
        self.handler.transport = self.transport
        self._enabled = True
        return self._enabled

    def is_enabled(self) -> bool:
        return self._enabled

    def send_initialize(self) -> None:
        if self.transport is None:
            return
        self.transport.send_json_rpc(method=INITIALIZE, params=({
            'capabilities': {
                'workspace': {
                    'workspaceFolders': True
                }
            }
        }))

    def send_set_editor_info(self) -> None:
        if self.transport is None:
            return
        self.transport.send_json_rpc(method=SET_EDITOR_INFO, params=({
            'editorInfo': {
                'name': 'sublime_text',
                'version': self.sublime_version
            },
            'editorPluginInfo': {
                'name': self.plugin_name,
                'version': self.copilot_version
            }
        }))

    def send_check_status(self, local_checks_only: bool = True) -> None:
        if self.transport is None:
            return
        self.transport.send_json_rpc(method=CHECK_STATUS, params=({
            'localChecksOnly': local_checks_only
        }), callback=self.handler._handle_check_status)

    def send_sign_in_initiate(self, callback) -> None:
        if self.transport is None:
            return
        self.transport.send_json_rpc(method=SIGN_IN_INITIATE, params=({}), callback=callback)

    def send_sign_in_confirm(self, user_code: str, callback):
        if self.transport is None:
            return
        self.transport.send_json_rpc(method=SIGN_IN_CONFIRM, params=({
            'userCode': user_code
        }), callback=callback)

    def send_sign_out(self) -> None:
        if self.transport is None:
            return
        self.transport.send_json_rpc(method=SIGN_OUT, params=({}))

    def send_get_completions(self, view: sublime.View, callback) -> None:
        if self.transport is None:
            return
        source = view.substr(sublime.Region(0, view.size()))
        language_id = view.syntax().scope.split('.')[-1]
        # this is all hacky
        request = {
            'doc': {
                'source': source,
                'tabSize': 2,
                'indentSize': 2,
                'insertSpaces': False,
                'path': view.buffer().file_name(),
                'uri': view.buffer().file_name(),
                'relativePath': view.buffer().file_name(),
                'languageId': language_id,
                'position': {
                    'line': view.rowcol(view.sel()[0].begin())[0],
                    'character': view.rowcol(view.sel()[0].end())[0],
                }
            }
        }
        
        self.transport.send_json_rpc(method=GET_COMPLETIONS, params=(request), callback=callback)

    def send_record_telemetry_consent(self, response: bool) -> None:
        pass

    def send_get_completions_cycling(self, advance: int) -> None:
        pass

    def send_notify_shown(self, uuid: str):
        if self.transport is None:
            return
        self.transport.send_json_rpc(method=NOTIFY_SHOWN, params=({
            'uuid': []
        }))

    def send_notify_rejected(self, uuids: List[str]):
        if self.transport is None:
            return
        self.transport.send_json_rpc(method=NOTIFY_REJECTED, params=({
            'uuids': []
        }))

    def send_notify_accepted(self):
        if self.transport is None:
            return
        self.transport.send_json_rpc(method=NOTIFY_ACCEPTED, params=({
            'uuid': []
        }))

copilot = Copilot()
