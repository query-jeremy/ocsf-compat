from typing import TypeVar, overload
from type_hell.model import OcsfModel, OcsfSchema, OcsfAttr, OcsfEvent
from type_hell.diff import DiffSchema, DiffAttr, DiffEvent, DiffModel



@overload
def create_diff(model: OcsfSchema) -> DiffSchema: ...

@overload
def create_diff(model: OcsfAttr) -> DiffAttr: ...

@overload
def create_diff(model: OcsfEvent) -> DiffEvent: ...


#T = TypeVar("T", bound=OcsfModel)
#def create_diff(model: T) -> ChangedModel[T]:
def create_diff(model: OcsfModel) -> DiffModel:

    match model:
        case OcsfSchema():
            return DiffSchema()
        case OcsfAttr():
            return DiffAttr()
        case OcsfEvent():
            return DiffEvent()
        case OcsfModel():
            raise ValueError("Why did you instantiate OcsfModel?!?")
        case _:
            raise ValueError("What model is this?!?")