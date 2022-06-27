from .core.registry import CopilotTextCommand
import sublime
import mdpopups


class CopilotEnableCommand(CopilotTextCommand):
    def run(self, _):
        if not self.copilot.start_copilot():
            sublime.message_dialog('failed to create a session')
        else:
            sublime.status_message("{}".format(self.copilot.plugin_name))

        self.copilot.send_initialize()
        self.copilot.send_set_editor_info()


class CopilotSignInCommand(CopilotTextCommand):
    def run(self, _):
        self.copilot.send_sign_in_initiate(self._handle_sign_in_response)

    def _handle_sign_in_response(self, obj) -> None:
        if obj is None:
            return
        # {'result': {'verificationUri': 'https://github.com/login/device', 'status': 'PromptUserDeviceFlow', 'userCode': '57B4-6102', 'expiresIn': 899, 'interval': 5}, 'jsonrpc': '2.0', 'id': '2'}
        results = obj.get('result', None)
        if results is None:
            print('no results from signin')
            return

        status = results.get('status', None)
        if status is None:
            print('no status from signin')
            return

        if status == 'AlreadySignedIn':
            self.copilot.signed_in = True
            return

        user_code = results.get('userCode', None)
        verification_uri = results.get('verificationUri', None)
        if user_code and verification_uri:
            if not sublime.ok_cancel_dialog('Login Required\nVisit: {}\nUser Code: {}\nPress OK when completed'.format(verification_uri, user_code)):
                self.copilot.signed_in = False
                return
            sublime.set_timeout_async(self.copilot.send_sign_in_confirm(user_code, self._handle_sign_in_confirm), 500)

    def _handle_sign_in_confirm(self, obj):
        if obj is None:
            return

        results = obj.get('result', None)
        if results is None:
            print('no results from signin confirm')
            return

        status = results.get('status', None)
        if status is None:
            print('no status from signin')
            return

        if status == 'OK':
            sublime.message_dialog('Successfully Signed In')
            self.copilot.signed_in = True


    def is_enabled(self) -> bool:
        return self.copilot.is_enabled()

    def is_visible(self) -> bool:
        return self.copilot.is_enabled() and not self.copilot.signed_in


class CopilotPreviewCompletionsCommand(CopilotTextCommand):
    def run(self, edit, completions, cycle: int = 0):
        if len(completions) == 0:
            return

        if cycle > len(completions)-1:
            cycle = 0

        syntax = self.view.syntax().scope.split('.')[-1]
        content = '<a href="{}">Accept Suggestion</a>\n```{}\n{}\n```'.format(cycle, syntax, completions[cycle]['displayText'])
        mdpopups.erase_phantoms(view=self.view, key='copilot.completion.previews')
        # This currently doesn't care about where the completion is actually supposed to be
        mdpopups.add_phantom(view=self.view, key='copilot.completion.previews', region=self.view.sel()[0], content=content, md=True, layout=sublime.LAYOUT_BELOW, on_navigate=self.insert_completion)

    def insert_completion(self, index):
        i = int(index)
        completion = self.copilot.current_completions[i]
        mdpopups.erase_phantoms(view=self.view, key='copilot.completion.previews')
        self.view.run_command('insert', {"characters": completion['displayText'].replace('\t', '')})

    def is_enabled(self) -> bool:
        return True

