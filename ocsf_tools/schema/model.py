from dataclasses import dataclass, field
from typing import Any, Optional, TypeVar
from abc import ABC


class OcsfModel(ABC): ...


@dataclass
class OcsfVersion(OcsfModel):
    version: str


@dataclass
class OcsfEnumMember(OcsfModel):
    caption: str
    description: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class OcsfDeprecationInfo(OcsfModel):
    message: str
    since: str


@dataclass
class OcsfType(OcsfModel):
    caption: str
    description: Optional[str] = None
    is_array: bool = False
    deprecated: Optional[OcsfDeprecationInfo] = None
    max_len: Optional[int] = None
    observable: Optional[int] = None
    range: Optional[list[int]] = None
    regex: Optional[str] = None
    type: Optional[str] = None
    type_name: Optional[str] = None
    values: Optional[list[Any]] = None


@dataclass
class OcsfAttr(OcsfModel):
    caption: str
    requirement: str
    type: str
    description: Optional[str] = None
    is_array: bool = False
    deprecated: Optional[OcsfDeprecationInfo] = None
    enum: Optional[dict[str, OcsfEnumMember]] = None
    group: Optional[str] = None
    observable: Optional[int] = None
    profile: Optional[str | list[str]] = None
    sibling: Optional[str] = None


@dataclass
class OcsfObject(OcsfModel):
    caption: str
    name: str
    description: Optional[str] = None
    attributes: dict[str, OcsfAttr] = field(default_factory=dict)
    extends: Optional[str] = None
    observable: Optional[int] = None
    profiles: Optional[list[str]] = None
    constraints: Optional[dict[str, list[str]]] = None
    deprecated: Optional[OcsfDeprecationInfo] = None


@dataclass
class OcsfEvent(OcsfModel):
    caption: str
    name: str
    attributes: dict[str, OcsfAttr] = field(default_factory=dict)
    description: Optional[str] = None
    uid: Optional[int] = None
    category: Optional[str] = None
    extends: Optional[str] = None
    profiles: Optional[list[str]] = None
    associations: Optional[dict[str, list[str]]] = None
    constraints: Optional[dict[str, list[str]]] = None
    deprecated: Optional[OcsfDeprecationInfo] = None


@dataclass
class OcsfSchema(OcsfModel):
    version: str
    classes: dict[str, OcsfEvent] = field(default_factory=dict)
    objects: dict[str, OcsfObject] = field(default_factory=dict)
    types: dict[str, OcsfType] = field(default_factory=dict)
    base_event: Optional[OcsfEvent] = None


OcsfT = TypeVar("OcsfT", bound=OcsfModel, covariant=True)

"""
@dataclass
class OcsfDictionaryTypes(OcsfModel):
    caption: str
    description: str
    attributes: OcsfAttributes = field(default_factory=dict)


@dataclass
class OcsfDictionary(OcsfModel):
    caption: str
    description: str
    name: str
    types: OcsfDictionaryTypes
    attributes: OcsfAttributes = field(default_factory=dict)


@dataclass
class OcsfCategory(OcsfModel):
    caption: str
    description: str
    uid: int
    type: Optional[str] = None


@dataclass
class OcsfCategories(OcsfModel):
    caption: str
    description: str
    name: str
    attributes: dict[str, OcsfCategory] = field(default_factory=dict)
"""
