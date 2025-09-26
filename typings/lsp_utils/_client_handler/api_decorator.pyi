from ..api_wrapper_interface import ApiWrapperInterface
from .interface import ClientHandlerInterface
from LSP.plugin.core.typing import Any, Callable, List, Union

__all__ = ['notification_handler', 'request_handler', 'register_decorated_handlers']

NotificationHandler = Callable[[Any, Any], None]
RequestHandler = Callable[[Any, Any, Callable[[Any], None]], None]
MessageMethods = Union[str, List[str]]

def notification_handler(notification_methods: MessageMethods) -> Callable[[NotificationHandler], NotificationHandler]: ...
def request_handler(request_methods: MessageMethods) -> Callable[[RequestHandler], RequestHandler]: ...
def register_decorated_handlers(client_handler: ClientHandlerInterface, api: ApiWrapperInterface) -> None: ...
