from .node_runtime import NodeRuntime
from .server_resource_interface import ServerResourceInterface
from LSP.plugin.core.typing import Dict, Optional
from _typeshed import Incomplete

__all__ = ['ServerNpmResource']

class ServerNpmResource(ServerResourceInterface):
    @classmethod
    def create(cls, options: ServerNpmResourceCreateOptions) -> ServerNpmResource: ...
    _status: Incomplete
    _package_name: Incomplete
    _package_storage: Incomplete
    _server_src: Incomplete
    _server_dest: Incomplete
    _binary_path: Incomplete
    _installation_marker_file: Incomplete
    _node_version_marker_file: Incomplete
    _node_runtime: Incomplete
    _skip_npm_install: Incomplete
    def __init__(self, package_name: str, server_directory: str, server_binary_path: str, package_storage: str, node_runtime: NodeRuntime, skip_npm_install: bool) -> None: ...
    @property
    def server_directory_path(self) -> str: ...
    @property
    def node_bin(self) -> str: ...
    @property
    def node_env(self) -> Optional[Dict[str, str]]: ...
    @property
    def binary_path(self) -> str: ...
    def get_status(self) -> int: ...
    def needs_installation(self) -> bool: ...
    def install_or_update(self) -> None: ...
