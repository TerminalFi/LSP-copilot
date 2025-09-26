from LSP.plugin.core.typing import Any, Callable
from abc import ABCMeta, abstractmethod

__all__ = ['ApiWrapperInterface']

NotificationHandler = Callable[[Any], None]
RequestHandler = Callable[[Any, Callable[[Any], None]], None]

class ApiWrapperInterface(metaclass=ABCMeta):
    @abstractmethod
    def on_notification(self, method: str, handler: NotificationHandler) -> None: ...
    @abstractmethod
    def on_request(self, method: str, handler: RequestHandler) -> None: ...
    @abstractmethod
    def send_notification(self, method: str, params: Any) -> None: ...
    @abstractmethod
    def send_request(self, method: str, params: Any, handler: Callable[[Any, bool], None]) -> None: ...
