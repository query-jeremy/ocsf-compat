
from typing import overload, TypeVar

from type_hell.diff import DiffModel, DiffSchema, DiffEvent, DiffAttr
from type_hell.model import OcsfModel, OcsfSchema, OcsfEvent, OcsfAttr
from type_hell.factory import create_diff


@overload
def compare(old_model: OcsfSchema, new_model: OcsfSchema) -> DiffSchema: ...

@overload
def compare(old_model: OcsfAttr, new_model: OcsfAttr) -> DiffAttr: ...

@overload
def compare(old_model: OcsfEvent, new_model: OcsfEvent) -> DiffEvent: ...


CompT = TypeVar("CompT", bound=OcsfModel)

#def compare(old_model: CompT, new_model: CompT) -> ChangedModel[CompT]:
def compare(old_model: OcsfModel, new_model: OcsfModel) -> DiffModel:
    assert type(old_model) == type(new_model)
    diff = create_diff(old_model)


    return diff