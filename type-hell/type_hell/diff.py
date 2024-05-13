from abc import ABC
from typing import TypeVar, Optional, Generic
from dataclasses import dataclass, field

from type_hell.model import OcsfName, OcsfAttr, OcsfEvent, OcsfSchema


T = TypeVar("T", covariant=True)


class Difference(Generic[T], ABC): ...


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

from model import OcsfModel
OcsfT = TypeVar("OcsfT", bound=OcsfModel, covariant=True)

class ChangedModel(Difference[OcsfT]): ...


@dataclass
class DiffAttr(ChangedModel[OcsfAttr]):
    caption: Difference[Optional[str]] = field(default_factory=NoChange[Optional[str]])
    max_len: Difference[Optional[int]] = field(default_factory=NoChange[Optional[int]])
    is_array: Difference[bool] = field(default_factory=NoChange[bool])

@dataclass
class DiffEvent(ChangedModel[OcsfEvent]):
    caption: Difference[str] = field(default_factory=NoChange[str])
    name: Difference[str] = field(default_factory=NoChange[str])
    uid: Difference[Optional[int]] = field(default_factory=NoChange[Optional[int]])
    attributes: dict[OcsfName, OcsfAttr] = field(default_factory=dict)

@dataclass
class DiffSchema(ChangedModel[OcsfSchema]):
    version: Difference[str] = field(default_factory=NoChange[str])
    classes: dict[OcsfName, OcsfAttr] = field(default_factory=dict)
    base_event: Difference[Optional[OcsfEvent]] = field(default_factory=NoChange[Optional[OcsfEvent]])
