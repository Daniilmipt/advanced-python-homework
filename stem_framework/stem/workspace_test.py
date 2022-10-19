# """
# Conception modularity software
# """
# import inspect
# from abc import abstractmethod, ABC, ABCMeta
# from importlib import import_module
# from types import ModuleType
# from typing import Optional, Any, TypeVar, Union
#
# from .core import Named
# from .meta import Meta
# from .task import Task
#
# T = TypeVar("T")
#
#
# class TaskPath:
#     def __init__(self, path: Union[str, list[str]]):
#         if isinstance(path, str):
#             self._path = path.split(".")
#         else:
#             self._path = path
#
#     @property
#     def is_leaf(self):
#         return len(self._path) == 1
#
#     @property
#     def sub_path(self):
#         return TaskPath(self._path[1:])
#
#     @property
#     def head(self):
#         return self._path[0]
#
#     @property
#     def name(self):
#         return self._path[-1]
#
#     def __str__(self):
#         return ".".join(self._path)
#
#
# class ProxyTask(Task[T]):
#
#     def __init__(self, proxy_name, task: Task):
#         self._name = proxy_name
#         self._task = task
#
#     @property
#     def dependencies(self):
#         return self._task.dependencies
#
#     @property
#     def specification(self):
#         return self._task.specification
#
#     def check_by_meta(self, meta: Meta):
#         self._task.check_by_meta(meta)
#
#     def transform(self, meta: Meta, /, **kwargs: Any) -> T:
#         return self._task.transform(meta, **kwargs)
#
#
# class IWorkspace(ABC, Named):
#     @property
#     @abstractmethod
#     def tasks(self) -> dict[str, Task]:
#         pass
#
#     @property
#     @abstractmethod
#     def workspaces(self) -> set["IWorkspace"]:
#         pass
#
#     def find_task(self, task_path: Union[str, TaskPath]) -> Optional[Task]:
#         if not isinstance(task_path, TaskPath):
#             task_path = TaskPath(task_path)
#         if task_path.is_leaf:
#             if task_path.name in self.tasks:
#                 for task in self.tasks:
#                     if task == task_path.name:
#                         return self.tasks[task]
#             for wrs in self.workspaces:
#                 # Создаю элемент этого пространства(wrs)
#                 # т.к. в workspace хранятся классы, а не их экземпляры
#                 task = wrs.find_task(task_path)
#                 if task is not None:
#                     return task
#             return None
#         else:
#             for wks in self.workspaces:
#                 if wks.name == task_path.head:
#                     return wks.find_task(task_path.sub_path)
#             return None
#
#     def has_task(self, task_path: Union[str, TaskPath]) -> bool:
#         return self.find_task(task_path) is not None
#
#     def get_workspace(self, name) -> Optional["IWorkspace"]:
#         for workspace in self.workspaces:
#             if workspace.name == name:
#                 return workspace
#         return None
#
#     def structure(self) -> dict:
#         return {
#             "name": self.name,
#             "tasks": list(self.tasks.keys()),
#             "workspaces": [w().structure() for w in self.workspaces]
#         }
#
#     @staticmethod
#     def find_default_workspace(task: Task) -> "IWorkspace":
#         """
#         Откуда у экземпляра класса Task должен быть аттрибут _stem_workspace?
#         :param task:
#         :return:
#         """
#         if hasattr(task, "_stem_workspace"):
#             return getattr(task, "_stem_workspace")
#         else:
#             module = import_module(task.__module__)
#             return IWorkspace.module_workspace(module)
#
#     @staticmethod
#     def module_workspace(module: ModuleType) -> "IWorkspace":
#         if hasattr(module, "_stem_workspace"):
#             return getattr(module, "_stem_workspace")
#         else:
#             name = module.__name__
#             tasks = {}
#             workspaces = []
#             for d in dir(module):
#                 cls = getattr(module, d)
#                             for s in dir(module):
#                 t = getattr(module, s)
#                 if issubclass(t, Task) or isinstance(t, Task):
#                     tasks[s] = t
#                 if (issubclass(t, type) or isinstance(t, type)) and \
#                         (issubclass(t, IWorkspace) or isinstance(t, IWorkspace)):
#                     workspaces.add(t)
#             setattr(module, "_stem_workspace", LocalWorkspace(name, tasks, workspaces))
#             return getattr(module, "_stem_workspace")
#
#
# class ILocalWorkspace(IWorkspace):
#     # @staticmethod
#     # def __subclasses__():
#     #     return [LocalWorkspace, Workspace, SubSubWorkspace, SubWorkspace, IntWorkspace]
#
#     @property
#     def tasks(self) -> dict[str, Task]:
#         return self._tasks
#
#     @property
#     def workspaces(self) -> set["IWorkspace"]:
#         return self._workspaces
#
#
# class LocalWorkspace(ILocalWorkspace):
#     def __init__(self, name, tasks=(), workspaces=()):
#         self._name = name
#         self._tasks = tasks
#         self._workspaces = workspaces
#
#
# class Workspace(ABCMeta, ILocalWorkspace):
#     def __new__(mcs, name, bases, attrs):
#         cls = super().__new__(ABCMeta, name, bases, attrs)
#         try:
#             workspaces = set(cls.workspaces)
#         except AttributeError:
#             workspaces = set()
#
#         if ILocalWorkspace not in bases:
#             bases += (ILocalWorkspace,)
#         cls = super().__new__(mcs, name, bases, attrs)
#         cls_attr = {a: t for a, t in cls.__dict__.items()}
#         cls_attr_replaced = {
#             a: ProxyTask(a, t)
#             for a, t in cls_attr.items()
#             if isinstance(t, Task) and not callable(t)
#         }
#         for a, t in cls_attr_replaced.items():
#             setattr(cls, a, t)
#
#         for a, t in cls.__dict__.items():
#             if isinstance(t, Task):
#                 t._stem_workspace = mcs
#
#         tasks = {a: t for a, t in cls.__dict__.items() if isinstance(t, Task)}
#         cls._workspaces = workspaces
#         cls._tasks = tasks
#         cls._name = name
#         return cls
from abc import ABC, abstractmethod, ABCMeta
from types import ModuleType
from typing import Dict, Optional, Any, Set, Type, TypeVar, Union
from importlib import import_module

from .core import Named
from .meta import Meta
from .task import Task

T = TypeVar("T")


class TaskPath:
    def __init__(self, path: Union[str, list[str]]):
        if isinstance(path, str):
            self._path = path.split(".")
        else:
            self._path = path

    @property
    def is_leaf(self):
        return len(self._path) == 1

    @property
    def sub_path(self):
        return TaskPath(self._path[1:])

    @property
    def head(self):
        return self._path[0]

    @property
    def name(self):
        return self._path[-1]

    def __str__(self):
        return ".".join(self._path)


class ProxyTask(Task[T]):

    def __init__(self, proxy_name, task: Task):
        self._name = proxy_name
        self._task = task

    @property
    def dependencies(self):
        return self._task.dependencies

    @property
    def specification(self):
        return self._task.specification

    def check_by_meta(self, meta: Meta):
        self._task.check_by_meta(meta)

    def transform(self, meta: Meta, /, **kwargs: Any) -> T:
        return self._task.transform(meta, **kwargs)


class IWorkspace(ABC, Named):
    @property
    @abstractmethod
    def tasks(self) -> dict[str, Task]:
        return self.tasks

    @property
    @abstractmethod
    def workspaces(self) -> set["IWorkspace"]:
        return self.workspaces

    def find_task(self, task_path: Union[str, TaskPath]) -> Optional[Task]:
        if not isinstance(task_path, TaskPath):
            task_path = TaskPath(task_path)
            if task_path.is_leaf:
                if task_path.name in self.tasks:
                    for task in self.tasks:
                        if task == task_path.name:
                            return self.tasks[task]
                for wrs in self.workspaces:
                    # Создаю элемент этого пространства(wrs)
                    # т.к. в workspace хранятся классы, а не их экземпляры
                    task = wrs.find_task(task_path)
                    if task is not None:
                        return task
                return None
            else:
                for wks in self.workspaces:
                    if wks.name == task_path.head:
                        return wks.find_task(task_path.sub_path)
                return None

    # @classmethod  # in tests, it is used as a @classmethod
    # def find_task(cls, task_path: Union[str, TaskPath]) -> Optional[Task]:
    #     if not isinstance(task_path, TaskPath):
    #         task_path = TaskPath(task_path)
    #     if not task_path.is_leaf:
    #         for w in cls.workspaces:
    #             if w.name == task_path.head:
    #                 return w.find_task(task_path.sub_path)
    #         return None
    #     else:
    #         for task_name in cls.tasks.keys():
    #             if task_name == task_path.name:
    #                 return cls.tasks[task_name]
    #         for w in cls.workspaces:
    #             if (t := w.find_task(task_path)) is not None:
    #                 return t
    #         return None

    # @classmethod
    # def has_task(cls, task_path: Union[str, TaskPath]) -> bool:
    #     return cls.find_task(task_path) is not None
    #
    # @classmethod
    # def get_workspace(cls, name) -> Optional["IWorkspace"]:
    #     for workspace in cls.workspaces:
    #         if workspace.name == name:
    #             return workspace
    #     return None

    def has_task(self, task_path: Union[str, TaskPath]) -> bool:
        return self.find_task(task_path) is not None

    def get_workspace(self, name) -> Optional["IWorkspace"]:
        for workspace in self.workspaces:
            if workspace.name == name:
                return workspace
        return None

    def structure(self) -> dict:
        return {
            "name": self.name,
            "tasks": list(self.tasks.keys()),
            "workspaces": [w.structure() for w in self.workspaces]
        }

    @staticmethod
    def find_default_workspace(task: Task) -> Type["IWorkspace"]:
        if hasattr(task, "_stem_workspace"):
            return getattr(task, "_stem_workspace")
        else:
            module = import_module(task.__module__)
        return IWorkspace.module_workspace(module)

    # def module_workspace(module: ModuleType) -> "IWorkspace":
    #     if hasattr(module, "_stem_workspace"):
    #         return getattr(module, "_stem_workspace")
    #     else:
    #         name = module.__name__
    #         tasks = {}
    #         workspaces = []
    #         for d in dir(module):
    #             cls = getattr(module, d)
    #                         for s in dir(module):
    #             t = getattr(module, s)
    #             if issubclass(t, Task) or isinstance(t, Task):
    #                 tasks[s] = t
    #             if (issubclass(t, type) or isinstance(t, type)) and \
    #                     (issubclass(t, IWorkspace) or isinstance(t, IWorkspace)):
    #                 workspaces.add(t)
    #         setattr(module, "_stem_workspace", LocalWorkspace(name, tasks, workspaces))
    #         return getattr(module, "_stem_workspace")
    @staticmethod
    def module_workspace(module: ModuleType) -> Type["IWorkspace"]:
        if hasattr(module, "__stem_workspace"):
            return module.__stem_workspace
        else:
            tasks = {}
            workspaces = []
            for s in dir(module):
                t = getattr(module, s)
                flag = True
                flag_arr = [True, True, True, True]
                try:
                    if issubclass(t, Task):
                        tasks[s] = t
                        flag = False
                except:
                    pass
                try:
                    if flag and isinstance(t, Task):
                        tasks[s] = t
                except:
                    pass

                try:
                    flag_arr[0] = issubclass(t, type)
                except:
                    flag_arr[0] = None
                try:
                    flag_arr[1] = isinstance(t, type)
                except:
                    flag_arr[1] = None
                try:
                    flag_arr[2] = issubclass(t, IWorkspace)
                except:
                    flag_arr[2] = None
                try:
                    flag_arr[3] = isinstance(t, IWorkspace)
                except:
                    flag_arr[3] = None

                if (flag_arr[0] or flag_arr[1]) and (flag_arr[2] or flag_arr[3]):
                    workspaces.append(t)

            setattr(module, "_stem_workspace", LocalWorkspace(module.__name__, tasks, workspaces))

            return getattr(module, "_stem_workspace")


class ILocalWorkspace(IWorkspace):
    # @staticmethod
    # def __subclasses__():
    #     return [LocalWorkspace, Workspace, SubSubWorkspace, SubWorkspace, IntWorkspace]

    @property
    def tasks(self) -> dict[str, Task]:
        return self._tasks

    @property
    def workspaces(self) -> set["IWorkspace"]:
        return self._workspaces


class LocalWorkspace(ILocalWorkspace):
    def __init__(self, name, tasks=(), workspaces=()):
        self._name = name
        self._tasks = tasks
        self._workspaces = workspaces


# class ILocalWorkspace(IWorkspace):
#     # @staticmethod
#     # def __subclasses__():
#     #     return [LocalWorkspace, Workspace, SubSubWorkspace, SubWorkspace, IntWorkspace]
#
#     @property
#     def tasks(self) -> dict[str, Task]:
#         return self._tasks
#
#     @property
#     def workspaces(self) -> set["IWorkspace"]:
#         return self._workspaces
def create_workspace(
        name: str, tasks: Dict[str, Task] = {},
        workspaces: Set[Type["IWorkspace"]] = set()
) -> type:
    return type(name, (IWorkspace,), {
        'name': name, 'tasks': tasks, 'workspaces': workspaces
    })
    # name, tasks and workspaces become class variables (not object fields),
    # thus we can use them in .find_task and .has_task


# I don't need classes Local and ILocal Workspace
#
# They are not valid workspaces
# because .tasks and .workspaces
# must be not @properties, but class variables
#
# class ILocalWorkspace(IWorkspace):

#     @property
#     def tasks(self) -> dict[str, Task]:
#         return self._tasks

#     @property
#     def workspaces(self) -> set["IWorkspace"]:
#         return self._workspaces


# class LocalWorkspace(ILocalWorkspace):

#     def __init__(self, name, tasks=(), workspaces=()):
#         self._name = name
#         self._tasks = tasks
#         self._workspaces = workspaces


class Workspace(ABCMeta, ILocalWorkspace):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(ABCMeta, name, bases, attrs)
        try:
            workspaces = set(cls.workspaces)
        except AttributeError:
            workspaces = set()

        if ILocalWorkspace not in bases:
            bases += (ILocalWorkspace,)
        cls = super().__new__(mcs, name, bases, attrs)
        cls_attr = {a: t for a, t in cls.__dict__.items()}
        cls_attr_replaced = {
            a: ProxyTask(a, t)
            for a, t in cls_attr.items()
            if isinstance(t, Task) and not callable(t)
        }
        for a, t in cls_attr_replaced.items():
            setattr(cls, a, t)

        for a, t in cls.__dict__.items():
            if isinstance(t, Task):
                t._stem_workspace = mcs

        tasks = {a: t for a, t in cls.__dict__.items() if isinstance(t, Task)}
        cls._workspaces = workspaces
        cls._tasks = tasks
        cls._name = name
        return cls
