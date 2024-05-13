from typing import TypeVar, overload, cast, Any, Type
from type_hell.model import OcsfModel, OcsfSchema, OcsfAttr, OcsfEvent
from type_hell.diff import Difference, DiffSchema, DiffAttr, DiffEvent, DiffModel, ChangedModel



@overload
def create_diff(model: OcsfSchema) -> DiffSchema: ...

@overload
def create_diff(model: OcsfAttr) -> DiffAttr: ...

@overload
def create_diff(model: OcsfEvent) -> DiffEvent: ...

#@overload
#def create_diff(model: OcsfModel) -> OcsfModel: ...

T = TypeVar("T", bound=OcsfModel, covariant=True)
#def create_diff(model: T) -> DiffModel: #ChangedModel[T]:
def create_diff(model: OcsfModel) -> DiffModel:
    match model:
        case OcsfSchema():
            #return cast(ChangedModel[T], DiffSchema())
            return DiffSchema()
        case OcsfAttr():
            return DiffAttr()
        case OcsfEvent():
            return DiffEvent()
        case OcsfModel():
            raise ValueError("Why did you instantiate OcsfModel?!?")
        case _:
            raise ValueError("Must be OcsfModel)")

