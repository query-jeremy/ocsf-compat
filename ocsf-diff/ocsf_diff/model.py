from dataclasses import dataclass, field
from typing import Any

from ocsf_schema import OcsfEnumValue, OcsfName


@dataclass
class Addition: ...


@dataclass
class Removal: ...


@dataclass
class Change:
    before: Any
    after: Any


Difference = Addition | Removal | Change | None


@dataclass
class DiffVersion:
    version: Difference = None


@dataclass
class DiffEnumMember:
    caption: Difference = None
    description: Difference = None
    notes: Difference = None


DiffEnum = dict[OcsfEnumValue, DiffEnumMember | Difference]


@dataclass
class DiffDeprecationInfo:
    message: Difference = None
    since: Difference = None


@dataclass
class DiffAttr:
    include: Difference = None
    caption: Difference = None
    default: Difference = None
    description: Difference = None
    enum: DiffEnum | Difference = None
    group: Difference = None
    is_array: Difference = None
    max_len: Difference = None
    name: Difference = None
    notes: Difference = None
    observable: Difference = None
    range: Difference = None
    regex: Difference = None
    requirement: Difference = None
    sibling: Difference = None
    type: Difference = None
    type_name: Difference = None
    profile: Difference = None
    values: Difference = None
    deprecated: DiffDeprecationInfo | Difference = None


DiffAttributes = dict[OcsfName, DiffAttr | Difference]


@dataclass
class DiffExtension:
    uid: Difference = None
    name: Difference = None
    caption: Difference = None
    path: Difference = None
    version: Difference = None
    description: Difference = None


@dataclass
class DiffDictionaryTypes:
    attributes: DiffAttributes = field(default_factory=dict)
    caption: Difference = None
    description: Difference = None


@dataclass
class DiffDictionary:
    attributes: DiffAttributes = field(default_factory=dict)
    caption: Difference = None
    description: Difference = None
    name: Difference = None
    types: DiffDictionaryTypes | Difference = None


@dataclass
class DiffCategory:
    caption: Difference = None
    description: Difference = None
    uid: Difference = None
    type: Difference = None


@dataclass
class DiffCategories:
    attributes: dict[OcsfName, DiffCategory | Difference] = field(default_factory=dict)
    caption: Difference = None
    description: Difference = None
    name: Difference = None


@dataclass
class DiffInclude:
    caption: Difference = None
    attributes: DiffAttributes = field(default_factory=dict)
    description: Difference = None
    annotations: Difference = None


@dataclass
class DiffProfile:
    caption: Difference = None
    description: Difference = None
    meta: Difference = None
    attributes: DiffAttributes = field(default_factory=dict)
    annotations: Difference = None


@dataclass
class DiffObject:
    caption: Difference = None
    name: Difference = None
    attributes: DiffAttributes = field(default_factory=dict)
    description: Difference = None
    extends: Difference = None
    observable: Difference = None
    profiles: Difference = None
    constraints: Difference = None
    include: Difference = None
    deprecated: DiffDeprecationInfo | Difference = None


@dataclass
class DiffEvent:
    caption: Difference = None
    name: Difference = None
    attributes: DiffAttributes = field(default_factory=dict)
    description: Difference = None
    uid: Difference = None
    category: Difference = None
    extends: Difference = None
    profiles: Difference = None
    associations: Difference = None
    constraints: Difference = None
    include: Difference = None
    deprecated: DiffDeprecationInfo | Difference = None


@dataclass
class DiffSchema:
    classes: dict[OcsfName, DiffEvent] = field(default_factory=dict)
    objects: dict[OcsfName, DiffObject] = field(default_factory=dict)
    version: Difference = None
    types: DiffAttributes | Difference = None
    base_event: DiffEvent | Difference = None


DiffModel = (
    DiffSchema
    | DiffDictionary
    | DiffCategories
    | DiffInclude
    | DiffProfile
    | DiffObject
    | DiffEvent
    | DiffExtension
    | DiffVersion
    | DiffAttr
    | DiffEnumMember
)
