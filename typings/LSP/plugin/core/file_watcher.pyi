from .protocol import FileChangeType as FileChangeType, WatchKind as WatchKind
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from typing import Protocol

DEFAULT_KIND: Incomplete
FileWatcherEventType: Incomplete
FilePath = str
FileWatcherEvent = tuple[FileWatcherEventType, FilePath]

def lsp_watch_kind_to_file_watcher_event_types(kind: WatchKind) -> list[FileWatcherEventType]: ...
def file_watcher_event_type_to_lsp_file_change_type(kind: FileWatcherEventType) -> FileChangeType: ...

class FileWatcherProtocol(Protocol):
    def on_file_event_async(self, events: list[FileWatcherEvent]) -> None: ...

class FileWatcher(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def create(cls, root_path: str, patterns: list[str], events: list[FileWatcherEventType], ignores: list[str], handler: FileWatcherProtocol) -> FileWatcher: ...
    @abstractmethod
    def destroy(self) -> None: ...

watcher_implementation: type[FileWatcher] | None

def register_file_watcher_implementation(file_watcher: type[FileWatcher]) -> None: ...
def get_file_watcher_implementation() -> type[FileWatcher] | None: ...
