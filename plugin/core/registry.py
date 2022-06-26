
from weakref import WeakSet
from weakref import WeakValueDictionary
from weakref import ref
from .typing import Iterable
from .typing import Optional
from .copilot import Copilot
from .copilot import copilot

import sublime
import sublime_plugin

def is_regular_view(v: sublime.View) -> bool:
    # Not from the quick panel (CTRL+P), and not a special view like a console, output panel or find-in-files panels.
    return not v.sheet().is_transient() and v.element() is None


class CopilotTextChangeListener(sublime_plugin.TextChangeListener):

    ids_to_listeners = WeakValueDictionary()  # type: WeakValueDictionary[int, CopilotTextChangeListener]

    @classmethod
    def is_applicable(cls, buffer: sublime.Buffer) -> bool:
        v = buffer.primary_view()
        return v is not None and is_regular_view(v)

    def __init__(self) -> None:
        super().__init__()
        self.view_listeners = WeakSet()  # type: WeakSet[DocumentSyncListener]

    def attach(self, buffer: sublime.Buffer) -> None:
        super().attach(buffer)
        if self.buffer is None:
            return
        self.ids_to_listeners[self.buffer.buffer_id] = self

    def detach(self) -> None:
        if self.buffer is None:
            return
        self.ids_to_listeners.pop(self.buffer.buffer_id, None)
        super().detach()

    def on_text_changed(self, changes: Iterable[sublime.TextChange]) -> None:
        if self.buffer is None:
            return
        view = self.buffer.primary_view()
        if not view:
            return
        change_count = view.change_count()
        frozen_listeners = WeakSet(self.view_listeners)

        def notify() -> None:
            for listener in list(frozen_listeners):
                listener.on_text_changed_async(change_count, changes)

        sublime.set_timeout_async(notify)

    def __repr__(self) -> str:
        if self.buffer is None:
            return "UNKNOWN"
        return "CopilotTextChangeListener({})".format(self.buffer.buffer_id)


class CopilotViewEventListener(sublime_plugin.ViewEventListener):
    ACTIVE_CLIENTS = 'livesession.active_clients'

    def __init__(self, view: sublime.View) -> None:
        super().__init__(view)
        self._text_change_listener = (
            None
        )  # type: Optional[ref[CopilotTextChangeListener]]
        self._copilot = None  # type: Optional[Copilot]
        self._registered = False

    def __del__(self) -> None:
        self.uid = None
        self.relative_name = None
        self.selection_set = []
        self.last_selection = sublime.Region(-1, -1)
        self.view.erase_status(self.ACTIVE_CLIENTS)
        self._deregister_view_async()

    @property
    def copilot(self) -> Copilot:
        if not self._copilot:
            self._copilot = copilot

        assert self._copilot
        return self._copilot

    def _register_async(self) -> bool:
        # self.workspace_ref = session_manager.add_view_to_session(
        #     self.view, self.view.settings().get('livesession.view.uid')
        # )
        # if not self.workspace_ref:
        #     # debug('not adding view to session')
        #     return False

        # self._file_name = self.workspace_ref['relative_name']
        # self.uid = self.view.settings().get('livesession.view.uid')
        buf = self.view.buffer()
        if not buf:
            # debug(f'not tracking bufferless view {self.view.id()}')
            return False

        text_change_listener = CopilotTextChangeListener.ids_to_listeners.get(
            buf.buffer_id
        )
        if not text_change_listener:
            # debug(f'couldn\'t find a text change listener for listener {self}')
            return False

        text_change_listener.view_listeners.add(self)
        self._text_change_listener = ref(text_change_listener)

        return True

    def on_load_async(self) -> None:
        if not self._registered and is_regular_view(self.view):
            self._register_async()

    def on_activated_async(self) -> None:
        if not self._registered and is_regular_view(self.view):
            self._register_async()

    def _deregister_view_async(self) -> None:
        pass
        # if self.manager.session_exists():
        #     self.manager.remove_view_from_session(self.uid)

    def on_text_changed_async(self, change_count, changes: Iterable[sublime.TextChange]) -> None:
        if self.copilot is None or not self.copilot.is_enabled():
            return
        self.copilot.send_get_completions(self.view)


class CopilotTextCommand(sublime_plugin.TextCommand):
    _copilot = None  # type: Optional[Copilot]

    @property
    def copilot(self) -> Copilot:
        if not self._copilot:
            self._copilot = copilot

        assert self._copilot
        return self._copilot

    def is_enabled(self) -> bool:
        return not self.copilot.is_enabled()

    def is_visible(self):
        return not self.copilot.is_enabled()

