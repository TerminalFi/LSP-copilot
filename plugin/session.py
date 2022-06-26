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
        self.copilot.send_check_status()



class CopilotPreviewCompletionsCommand(CopilotTextCommand):
    def run(self, edit, completions):
        self.completions = completions
        if len(self.completions) == 0:
            return

        syntax = self.view.syntax().scope.split('.')[-1]
        content = '```{}\n{}\n```'.format(syntax, self.completions[0]['displayText'])
        mdpopups.erase_phantoms(view=self.view, key='copilot.completion.previews')
        mdpopups.add_phantom(view=self.view, key='copilot.completion.previews', region=self.view.sel()[0], content=content, md=True, layout=sublime.LAYOUT_BELOW)

    def is_enabled(self) -> bool:
        return True


