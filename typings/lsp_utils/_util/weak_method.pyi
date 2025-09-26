from LSP.plugin.core.typing import Any, Callable

__all__ = ['weak_method']

def weak_method(method: Callable[..., Any]) -> Callable[..., Any]: ...
