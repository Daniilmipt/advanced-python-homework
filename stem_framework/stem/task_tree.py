from typing import TypeVar, Optional, Generic

from .task import Task
from .workspace import IWorkspace

T = TypeVar("T")


class TaskNode(Generic[T]):
    def __init__(self, task: Task[T], workspace: Optional[IWorkspace] = None):
        self.task = task
        if workspace is None:
            wrs = IWorkspace.find_default_workspace(task)
        else:
            wrs = workspace
        self.workspace = wrs

    @property
    def dependencies(self) -> list["TaskNode"]:
        resolved_dependencies = []
        for d in self.task.dependencies:
            if self.workspace.has_task(d):
                resolved_dependencies.append(
                    TaskNode(self.workspace.find_task(d), self.workspace)
                )
        return resolved_dependencies

    @property
    def is_leaf(self) -> bool:
        if self.dependencies:
            return False
        else:
            return True

    @property
    def unresolved_dependencies(self) -> list["str"]:
        unresolved_dependencies = []
        for d in self.task.dependencies:
            if not self.workspace.has_task(d):
                unresolved_dependencies.append(d)
        return unresolved_dependencies

    @property
    def has_dependence_errors(self) -> bool:
        flag = False
        if self.unresolved_dependencies:
            return True
        if not flag:
            for d in self.dependencies:
                flag = d.has_dependence_errors
                if flag:
                    return True
        return flag


class TaskTree:

    def __init__(self, root: Task, workspace=None):
        self.root = TaskNode(root, workspace)

    def find_task(self, task, workspace=None) -> TaskNode[T]:
        if workspace is None:
            wrs = IWorkspace.find_default_workspace(task)
        else:
            wrs = workspace

        if task == self.root.task and self.root.workspace == wrs:
            return self.root
        else:
            for dep in self.root.dependencies:
                tree = TaskTree(dep.task, dep.workspace)
                node = tree.find_task(task, workspace)
                if node is not None:
                    return node
        return None

    def resolve_node(self, task: Task[T], workspace: Optional[IWorkspace] = None) -> TaskNode[T]:
        if workspace is None:
            wrs = IWorkspace.find_default_workspace(task)
        else:
            wrs = workspace

        node = self.find_task(task, wrs)
        if node is None:
            return TaskNode(task, workspace)
        else:
            return node
