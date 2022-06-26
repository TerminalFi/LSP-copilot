import sublime
from .typing import Union
from .types import INITIALIZE
from .types import SET_EDITOR_INFO
from .types import CHECK_STATUS
from .types import SIGN_IN_INITIATE
from .types import SIGN_IN_CONFIRM
from .types import SIGN_OUT
from .types import GET_COMPLETIONS
from .types import RECORD_TELEMETRY_CONSENT
from .types import GET_COMPLETIONS_CYCLING
from .types import NOTIFY_SHOWN
from .types import NOTIFY_REJECTED
from .types import NOTIFY_ACCEPTED
from .types import LOG_MESSAGE
from .types import STATUS_NOTIFICATION
from .typing import Any
from .typing import Dict
from .typing import Optional

from .rpc import Transport


class Handler:
    def __init__(self) -> None:
        self.transport = None # type: Transport[Dict[str, Any]]

    def on_transport_close(self, exit_code: int, exception: Optional[Exception]):
        pass

    def on_payload(self, method: str, payload: Dict):
        if method == INITIALIZE:
            self._handle_initialize(obj=payload)
        elif method == SET_EDITOR_INFO:
            self._handle_set_editor_info(obj=payload)
        elif method == CHECK_STATUS:
            self._handle_check_status(obj=payload)
        elif method == SIGN_IN_INITIATE:
            self._handle_sign_in_initiate(obj=payload)
        elif method == SIGN_IN_CONFIRM:
            self._handle_sign_in_confirm(obj=payload)
        elif method == SIGN_OUT:
            self._handle_sign_out(obj=payload)
        elif method == GET_COMPLETIONS:
            self._handle_get_completions(obj=payload)
        elif method == RECORD_TELEMETRY_CONSENT:
            self._handle_record_telemetry_consent(obj=payload)
        elif method == GET_COMPLETIONS_CYCLING:
            self._handle_get_completions_cycling(obj=payload)
        elif method == NOTIFY_SHOWN:
            self._handle_notify_shown(obj=payload)
        elif method == NOTIFY_REJECTED:
            self._handle_notify_rejected(obj=payload)
        elif method == NOTIFY_ACCEPTED:
            self._handle_notify_accepted(obj=payload)
        elif method == LOG_MESSAGE:
            pass
            # print(payload.get('params').get('message'))
        elif method == STATUS_NOTIFICATION:
            pass
            # print(payload.get('params').get('status'))
        else:
            sublime.set_timeout_async(print('unknown method {}'.format(method)), 0)


        # result = payload.get('result', None)
        # if result is None:
        #     return None

        # if isinstance(result, dict):
        #     kind = result.get('status', None)
        #     if kind is None:
        #         return
        #     user_code = None
        #     if kind == 'PromptUserDeviceFlow':
        #         print(result)
        #         user_code = result.get('userCode', None)

        #     if user_code is None:
        #         return

        #     input('Hit enter after login')
        #     self.transport.send_json_rpc(method='signInConfirm', params=({'userCode': user_code}))

    def on_stderr_message(self, data):
        sublime.set_timeout_async(print(data), 0)

    def _handle_initialize(self, obj: Dict) -> None:
        # {
        #     "jsonrpc": "2.0",
        #     "id": 0,
        #     "method": "client/registerCapability",
        #     "params": {
        #         "registrations": [
        #             {
        #                 "id": "063b3d74-7ea6-4f4c-a16a-883f0364a2ed",
        #                 "method": "workspace/didChangeWorkspaceFolders",
        #                 "registerOptions": {}
        #             }
        #         ]
        #     }
        # }
        # {
        #     "jsonrpc": "2.0",
        #     "id": "0",
        #     "result": {
        #         "capabilities": {
        #             "textDocumentSync": {
        #                 "openClose": True,
        #                 "change": 2
        #             },
        #             "workspace": {
        #                 "workspaceFolders": {
        #                     "supported": True,
        #                     "changeNotifications": True
        #                 }
        #             }
        #         }
        #     }
        # }
        pass

    def _handle_set_editor_info(self, obj: Dict) -> bool:
        # {'jsonrpc': '2.0', 'id': '1', 'result': 'OK'}
        return bool(obj.get('result', None) == 'OK')

    def _handle_check_status(self, obj: Dict) -> Union[str, None]:
        # {'jsonrpc': '2.0', 'id': '3', 'result': {'status': 'OK', 'user': 'TheSecEng'}}
        results = obj.get('result', {})
        status = results.get('status', None)
        user = results.get('user', None)
        sublime.set_timeout_async(print(user), 0)
        if bool(status == 'OK'):
            return user
        return None

    def _handle_sign_in_initiate(self, obj: Dict) -> bool:
        # {'jsonrpc': '2.0', 'id': '2', 'result': {'status': 'AlreadySignedIn', 'user': 'TheSecEng'}}
        results = obj.get('result', {})
        status = results.get('status', None)
        if status == 'AlreadySignedIn':
            return True
        else:
            False

    def _handle_sign_in_confirm(self, obj: Dict) -> None:
        pass

    def _handle_sign_out(self, obj: Dict) -> None:
        pass

    def _handle_get_completions(self, obj: Dict) -> None:
        completions = obj.get('result', {'completions':[]}).get('completions')
        window = sublime.active_window()
        view = window.active_view()
        sublime.set_timeout_async(view.run_command('copilot_preview_completions', {'completions': completions}), 0)

    def _handle_record_telemetry_consent(self, obj: Dict) -> None:
        pass

    def _handle_get_completions_cycling(self, obj: Dict) -> None:
        pass

    def _handle_notify_shown(self, obj: Dict) -> None:
        pass

    def _handle_notify_rejected(self, obj: Dict) -> None:
        pass

    def _handle_notify_accepted(self, obj: Dict) -> None:
        pass

