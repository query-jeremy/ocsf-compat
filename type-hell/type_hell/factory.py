from typing import TypeVar, overload
from type_hell.model import OcsfModel, OcsfSchema, OcsfAttr, OcsfEvent
from type_hell.diff import ChangedModel, DiffSchema, DiffAttr, DiffEvent


T = TypeVar("T", bound=OcsfModel)

@overload
def create_diff(model: OcsfSchema) -> DiffSchema: ...

@overload
def create_diff(model: OcsfAttr) -> DiffAttr: ...

@overload
def create_diff(model: OcsfEvent) -> DiffEvent: ...

def create_diff(model: T) -> ChangedModel[T]:
    match model:
        case OcsfSchema():
            return DiffSchema()
        case OcsfAttr():
            return DiffAttr()
        case OcsfEvent():
            return DiffEvent()
        case _:
            raise ValueError("What model is this?!?")