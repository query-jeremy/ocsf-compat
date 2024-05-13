from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

OcsfName = str

class OcsfModel(ABC): ...

@dataclass
class OcsfAttr(OcsfModel):
    caption: Optional[str] = None
    is_array: bool = False
    max_len: Optional[int] = None

@dataclass
class OcsfEvent(OcsfModel):
    caption: str
    name: str
    uid: Optional[int] = None
    attributes: dict[OcsfName, OcsfAttr] = field(default_factory=dict)

@dataclass
class OcsfSchema(OcsfModel):
    version: str
    classes: dict[OcsfName, OcsfEvent] = field(default_factory=dict)
    base_event: Optional[OcsfEvent] = None