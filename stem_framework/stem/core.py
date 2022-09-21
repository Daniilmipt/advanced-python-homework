from typing import Optional, Any, Protocol
import re


def pascal_case_to_snake_case(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class Named:
    _name: Optional[str] = None

    @property
    def name(self):
        if self._name is not None:
            return self._name
        else:
            return pascal_case_to_snake_case(self.__class__.__name__)


class Dataclass(Protocol):
    __dataclass_fields__: Any
