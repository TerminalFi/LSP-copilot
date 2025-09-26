from .generic_client_handler import GenericClientHandler
from .server_pip_resource import ServerPipResource
from .server_resource_interface import ServerResourceInterface
from LSP.plugin.core.typing import List, Optional

__all__ = ['PipClientHandler']

class PipClientHandler(GenericClientHandler):
    __server: Optional[ServerPipResource]
    requirements_txt_path: str
    server_filename: str
    @classmethod
    def get_python_binary(cls) -> str: ...
    @classmethod
    def manages_server(cls) -> bool: ...
    @classmethod
    def get_server(cls) -> Optional[ServerResourceInterface]: ...
    @classmethod
    def get_additional_paths(cls) -> List[str]: ...
