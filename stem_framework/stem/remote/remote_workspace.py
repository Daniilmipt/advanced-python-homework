import socket
from typing import Any, TypeVar

from stem.meta import Meta
from stem.task import Task
from stem.workspace import IWorkspace

T = TypeVar("T")


class RemoteTask(Task):

    def transform(self, meta: Meta, /, **kwargs: Any) -> T:
        pass  # TODO(Assignment 10)


class RemoteWorkspace(IWorkspace):

    def __init__(self, address="localhost", port=8888):
        self.address = address
        self.port = port

    @property
    def tasks(self) -> dict[str, Task]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.address, self.port))

    @property
    def workspaces(self) -> set["IWorkspace"]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.address, self.port))
