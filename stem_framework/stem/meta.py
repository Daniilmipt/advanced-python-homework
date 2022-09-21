"""
Description conception of metadata and metadata processor
"""
from dataclasses import dataclass, is_dataclass
from typing import Optional, Any, Union
from stem.core import Dataclass

Meta = Union[dict, Dataclass]

SpecificationField = tuple[object, Union[type, tuple[type, ...]]]
Specification = Union[Dataclass, SpecificationField, tuple[SpecificationField, ...]]


class SpecificationError(Exception):
    pass


@dataclass
class MetaFieldError:
    required_key: str
    required_types: Optional[tuple[type]] = None
    presented_type: Optional[type] = None
    presented_value: Any = None


class MetaVerification:
    def __init__(self, *errors: Union[MetaFieldError, "MetaVerification"]):
        self.error = errors
        self.checked_success = errors == []

    @staticmethod
    def verify(meta: Meta,
               specification: Optional[Specification] = None) -> "MetaVerification":

        if is_dataclass(specification):
            spec_keys = specification.__dataclass_fields__.keys()
            spec_dc = {k: specification.__dataclass_fields__[k].type for k in spec_keys}
        else:
            spec_keys = dict([specification]).keys()
            spec_dc = dict([specification])

        if is_dataclass(meta):
            meta_keys = meta.__dataclass_fields__.keys()
        else:
            meta_keys = meta.keys()

        errors: list[Union[MetaFieldError, "MetaVerification"]] = []
        for spec_key in spec_keys:
            if isinstance(spec_key, tuple):
                errors += MetaVerification.verify(meta, spec_key).error
            else:
                if spec_key not in meta_keys:
                    errors.append(
                        MetaFieldError(spec_key,
                                       spec_dc[spec_key]
                                       )
                    )
                elif issubclass(type(get_meta_attr(meta, spec_key)), spec_dc[spec_key]):
                    pass
                else:
                    errors.append(
                        MetaFieldError(spec_key,
                                       spec_dc[spec_key],
                                       get_meta_attr(meta, spec_key),
                                       type(get_meta_attr(meta, spec_key))
                                       )
                    )
        return MetaVerification(*errors)


def get_meta_attr(meta: Meta, key: str, default: Optional[Any] = None) -> Optional[Any]:
    try:
        return meta[key]
    except KeyError:
        return default
    except TypeError:
        pass

    try:
        return getattr(meta, key)
    except AttributeError:
        return default


def update_meta(meta: Meta, **kwargs):
    for key in kwargs:
        setattr(meta, key, kwargs[key])
