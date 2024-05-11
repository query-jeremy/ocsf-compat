"""Model for comparing OCSF schemata

Notes:
 - Everything inherits from Difference[T]
 - None has been replaced with NoChange[T]
 - Dicts of [str, OcsfModel] always have all keys from both operands.
 - Be warned that OcsfAttr.enum is Optional[dict[str, OcsfEnumMember]] and so it may be NoChange[OcsfEnumMember] instead of an empty dict.
 - Dicts of primitives:
    - OcsfInclude.annotations
    - OcsfProfile.annotations
    - OcsfObject.constraints
    - OcsfEvent.constraints
"""

from dataclasses import dataclass, field
from typing import Any, TypeVar, Generic, Optional

from ocsf_schema import (
    OcsfEnumValue,
    OcsfName,
    OcsfVersion,
    OcsfEnum,
    OcsfEnumMember,
    OcsfAttr,
    OcsfDeprecationInfo,
    OcsfExtension,
    OcsfDictionary,
    OcsfDictionaryTypes,
    OcsfCategory,
    OcsfCategories,
    OcsfInclude,
    OcsfProfile,
    OcsfObject,
    OcsfEvent,
    OcsfSchema,
)


T = TypeVar("T")


class Difference(Generic[T]): ...


@dataclass
class Addition(Difference[T]):
    after: T


@dataclass
class Removal(Difference[T]):
    before: T


@dataclass
class Change(Difference[T]):
    before: Optional[T]
    after: Optional[T]


@dataclass
class NoChange(Difference[T]): ...


class ChangedModel(Difference[T]): ...


@dataclass
class DiffVersion(ChangedModel[OcsfVersion]):
    version: Difference[str] = field(default_factory=NoChange[str])


@dataclass
class DiffEnumMember(ChangedModel[OcsfEnumMember]):
    caption: Difference[str] = field(default_factory=NoChange[str])
    description: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    notes: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])


DiffEnum = dict[OcsfEnumValue, Difference[OcsfEnumMember]]


@dataclass
class DiffDeprecationInfo(ChangedModel[OcsfDeprecationInfo]):
    message: Difference[str] = field(default_factory=NoChange[str])
    since: Difference[str] = field(default_factory=NoChange[str])


@dataclass
class DiffAttr(ChangedModel[OcsfAttr]):
    include: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    caption: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    default: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    description: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    enum: Difference[Optional[OcsfEnum]] = field(default_factory=NoChange[Optional[OcsfEnum]])
    group: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    is_array: Difference[Optional[bool]] = field(default_factory=NoChange[Optional[bool]])
    max_len: Difference[Optional[int]] = field(default_factory=NoChange[Optional[int]])
    name: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    notes: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    observable: Difference[Optional[int]] = field(default_factory=NoChange[Optional[int]])
    range: Difference[Optional[list[int]]] = field(default_factory=NoChange[Optional[list[int]]])
    regex: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    requirement: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    sibling: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    type: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    type_name: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    profile: Difference[Optional[str | list[str]]] = field(default_factory=NoChange[Optional[str | list[str]]])
    values: Difference[Optional[list[Any]]] = field(default_factory=NoChange[Optional[list[Any]]])
    deprecated: Difference[Optional[OcsfDeprecationInfo]] = field(
        default_factory=NoChange[Optional[OcsfDeprecationInfo]]
    )


DiffAttributes = dict[OcsfName, Difference[OcsfAttr]]


@dataclass
class DiffExtension(ChangedModel[OcsfExtension]):
    uid: Difference[int] = field(default_factory=NoChange[int])
    name: Difference[str] = field(default_factory=NoChange[str])
    caption: Difference[str] = field(default_factory=NoChange[str])
    path: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    version: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    description: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])


@dataclass
class DiffDictionaryTypes(ChangedModel[OcsfDictionaryTypes]):
    attributes: DiffAttributes = field(default_factory=dict)
    caption: Difference[str] = field(default_factory=NoChange[str])
    description: Difference[str] = field(default_factory=NoChange[str])


@dataclass
class DiffDictionary(ChangedModel[OcsfDictionary]):
    attributes: DiffAttributes = field(default_factory=dict)
    caption: Difference[str] = field(default_factory=NoChange[str])
    description: Difference[str] = field(default_factory=NoChange[str])
    name: Difference[str] = field(default_factory=NoChange[str])
    types: Difference[OcsfDictionaryTypes] = field(default_factory=NoChange[OcsfDictionaryTypes])


@dataclass
class DiffCategory(ChangedModel[OcsfCategory]):
    caption: Difference[str] = field(default_factory=NoChange[str])
    description: Difference[str] = field(default_factory=NoChange[str])
    uid: Difference[int] = field(default_factory=NoChange[int])
    type: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])


@dataclass
class DiffCategories(ChangedModel[OcsfCategories]):
    attributes: dict[OcsfName, Difference[OcsfCategory]] = field(default_factory=dict)
    caption: Difference[str] = field(default_factory=NoChange[str])
    description: Difference[str] = field(default_factory=NoChange[str])
    name: Difference[str] = field(default_factory=NoChange[str])


@dataclass
class DiffInclude(ChangedModel[OcsfInclude]):
    caption: Difference[str] = field(default_factory=NoChange[str])
    attributes: DiffAttributes = field(default_factory=dict)
    description: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    annotations: Difference[dict[str, str]] = field(default_factory=NoChange[dict[str, str]])


@dataclass
class DiffProfile(ChangedModel[OcsfProfile]):
    caption: Difference[str] = field(default_factory=NoChange[str])
    description: Difference[str] = field(default_factory=NoChange[str])
    meta: Difference[str] = field(default_factory=NoChange[str])
    attributes: DiffAttributes = field(default_factory=dict)
    annotations: Difference[dict[str, str]] = field(default_factory=NoChange[dict[str, str]])


@dataclass
class DiffObject(ChangedModel[OcsfObject]):
    caption: Difference[str] = field(default_factory=NoChange[str])
    name: Difference[OcsfName] = field(default_factory=NoChange[OcsfName])
    attributes: DiffAttributes = field(default_factory=dict)
    description: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    extends: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    observable: Difference[Optional[int]] = field(default_factory=NoChange[Optional[int]])
    profiles: Difference[Optional[list[str]]] = field(default_factory=NoChange[Optional[list[str]]])
    constraints: Difference[Optional[dict[str, list[str]]]] = field(
        default_factory=NoChange[Optional[dict[str, list[str]]]]
    )
    include: Difference[Optional[str | list[str]]] = field(default_factory=NoChange[Optional[str | list[str]]])
    deprecated: Difference[Optional[OcsfDeprecationInfo]] = field(
        default_factory=NoChange[Optional[OcsfDeprecationInfo]]
    )


@dataclass
class DiffEvent(ChangedModel[OcsfEvent]):
    caption: Difference[str] = field(default_factory=NoChange[str])
    name: Difference[str] = field(default_factory=NoChange[str])
    attributes: DiffAttributes = field(default_factory=dict)
    description: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    uid: Difference[int] = field(default_factory=NoChange[int])
    category: Difference[str] = field(default_factory=NoChange[str])
    extends: Difference[str] = field(default_factory=NoChange[str])
    profiles: Difference[list[str]] = field(default_factory=NoChange[list[str]])
    associations: Difference[dict[str, list[str]]] = field(default_factory=NoChange[dict[str, list[str]]])
    constraints: Difference[dict[str, list[str]]] = field(default_factory=NoChange[dict[str, list[str]]])
    include: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    deprecated: Difference[Optional[OcsfDeprecationInfo]] = field(
        default_factory=NoChange[Optional[OcsfDeprecationInfo]]
    )


@dataclass
class DiffSchema(ChangedModel[OcsfSchema]):
    classes: dict[OcsfName, Difference[OcsfEvent]] = field(default_factory=dict)
    objects: dict[OcsfName, Difference[OcsfObject]] = field(default_factory=dict)
    version: Difference[OcsfVersion] = field(default_factory=NoChange[OcsfVersion])
    types: DiffAttributes = field(default_factory=dict)
    base_event: Difference[Optional[OcsfEvent]] = field(default_factory=NoChange[Optional[OcsfEvent]])


DiffModel = (
    DiffSchema
    | DiffDictionary
    | DiffDictionaryTypes
    | DiffCategories
    | DiffInclude
    | DiffProfile
    | DiffObject
    | DiffEvent
    | DiffExtension
    | DiffVersion
    | DiffAttr
    | DiffEnumMember
    | DiffDeprecationInfo
)

OcsfComparable = TypeVar(
    "OcsfComparable",
    OcsfSchema,
    OcsfEvent,
    OcsfObject,
    OcsfAttr,
    OcsfDeprecationInfo,
    OcsfDictionary,
    OcsfDictionaryTypes,
    OcsfCategories,
    OcsfInclude,
    OcsfProfile,
    OcsfExtension,
    OcsfVersion,
    OcsfEnumMember,
)

OcsfComparableU = (
    OcsfSchema
    | OcsfEvent
    | OcsfObject
    | OcsfAttr
    | OcsfDeprecationInfo
    | OcsfDictionary
    | OcsfDictionaryTypes
    | OcsfCategories
    | OcsfInclude
    | OcsfProfile
    | OcsfExtension
    | OcsfVersion
    | OcsfEnumMember,
)

# TODO would be nice to get these by introspecting OcsfComparable
COMPARABLE_TYPES: tuple[type, ...] = (
    OcsfSchema,
    OcsfEvent,
    OcsfObject,
    OcsfAttr,
    OcsfDeprecationInfo,
    OcsfDictionary,
    OcsfDictionaryTypes,
    OcsfCategories,
    OcsfInclude,
    OcsfProfile,
    OcsfExtension,
    OcsfVersion,
    OcsfEnumMember,
)
