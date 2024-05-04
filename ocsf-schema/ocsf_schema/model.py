from dataclasses import dataclass

from typing import (
    Any,
    Optional,
)

OcsfEnumValue = str
OcsfName = str


@dataclass
class OcsfVersion:
    version: str


@dataclass
class OcsfEnumMember:
    caption: str
    description: Optional[str] = None
    notes: Optional[str] = None


OcsfEnum = dict[OcsfEnumValue, OcsfEnumMember]


@dataclass
class OcsfDeprecationInfo:
    message: str
    since: str


@dataclass
class OcsfAttr:
    include: Optional[str] = None
    caption: Optional[str] = None
    default: Optional[Any] = None
    description: Optional[str] = None
    enum: Optional[OcsfEnum] = None
    group: Optional[str] = None
    is_array: bool = False
    max_len: Optional[int] = None
    name: Optional[str] = None
    notes: Optional[str] = None
    observable: Optional[int] = None
    range: Optional[list[int]] = None
    regex: Optional[str] = None
    requirement: Optional[str] = None
    sibling: Optional[str] = None
    type: Optional[str] = None
    type_name: Optional[str] = None
    profile: Optional[str | list[str]] = None
    values: Optional[list[Any]] = None
    deprecated: Optional[OcsfDeprecationInfo] = None


OcsfAttributes = dict[OcsfName, OcsfAttr]


@dataclass
class OcsfExtension:
    uid: int
    name: OcsfName
    caption: str
    path: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None


@dataclass
class OcsfDictionaryTypes:
    attributes: OcsfAttributes
    caption: str
    description: str


@dataclass
class OcsfDictionary:
    attributes: OcsfAttributes
    caption: str
    description: str
    name: OcsfName
    types: OcsfDictionaryTypes


@dataclass
class OcsfCategory:
    caption: str
    description: str
    uid: int
    type: Optional[str] = None


@dataclass
class OcsfCategories:
    attributes: dict[OcsfName, OcsfCategory]
    caption: str
    description: str
    name: OcsfName


@dataclass
class OcsfInclude:
    caption: str
    attributes: OcsfAttributes
    description: Optional[str] = None
    annotations: Optional[dict[str, str]] = None


@dataclass
class OcsfProfile:
    caption: str
    description: str
    meta: str
    attributes: OcsfAttributes
    annotations: Optional[dict[str, str]] = None


@dataclass
class OcsfObject:
    caption: str
    name: OcsfName
    attributes: OcsfAttributes
    description: Optional[str] = None
    extends: Optional[str] = None
    observable: Optional[int] = None
    profiles: Optional[list[str]] = None
    constraints: Optional[dict[str, list[str]]] = None
    include: Optional[str | list[str]] = None
    deprecated: Optional[OcsfDeprecationInfo] = None


@dataclass
class OcsfEvent:
    caption: str
    name: OcsfName
    attributes: OcsfAttributes
    description: Optional[str] = None
    uid: Optional[int] = None
    category: Optional[str] = None
    extends: Optional[str] = None
    profiles: Optional[list[str]] = None
    associations: Optional[dict[str, list[str]]] = None
    constraints: Optional[dict[str, list[str]]] = None
    include: Optional[str] = None
    deprecated: Optional[OcsfDeprecationInfo] = None


@dataclass
class OcsfSchema:
    version: str
    classes: dict[OcsfName, OcsfEvent]
    objects: dict[OcsfName, OcsfObject]
    types: OcsfAttributes
    base_event: Optional[OcsfEvent] = None


OcsfModel = (
    OcsfSchema
    | OcsfEvent
    | OcsfObject
    | OcsfDeprecationInfo
    | OcsfAttr
    | OcsfEnumMember
    | OcsfVersion
    | OcsfExtension
    | OcsfDictionaryTypes
    | OcsfDictionary
    | OcsfCategory
    | OcsfCategories
    | OcsfInclude
    | OcsfProfile
)
