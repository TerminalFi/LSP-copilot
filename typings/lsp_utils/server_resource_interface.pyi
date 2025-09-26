import abc
from abc import ABCMeta, abstractmethod

__all__ = ['ServerStatus', 'ServerResourceInterface']

class ServerStatus:
    UNINITIALIZED: int
    ERROR: int
    READY: int

class ServerResourceInterface(metaclass=ABCMeta):
    @abstractmethod
    def needs_installation(self) -> bool: ...
    @abstractmethod
    def install_or_update(self) -> None: ...
    @abstractmethod
    def get_status(self) -> int: ...
    @property
    @abc.abstractmethod
    def binary_path(self) -> str: ...
