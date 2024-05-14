
from typing import TypeVar, get_type_hints, get_origin, cast, get_args, Union, Any, TypeGuard
from types import UnionType, NoneType

from type_hell.diff import DiffSchema, DiffEvent, DiffAttr, Difference, NoChange, Addition, Removal, Change, ChangedModel
from type_hell.model import OcsfModel, OcsfSchema, OcsfEvent, OcsfAttr


K = TypeVar("K")
T = TypeVar("T")

def compare_dict(old_val: dict[K, T] | None, new_val: dict[K, T] | None) -> dict[K, Difference[T]]:
    if old_val is None:
        old_val = {}

    if new_val is None:
        new_val = {}

    ret: dict[K, Difference[T]] = {}
    keys: set[K] = set(old_val.keys()) | set(new_val.keys())    

    for key in keys:
        if key not in new_val:
            ret[key] = Removal(before=old_val[key])
        elif key not in old_val:
            ret[key] = Addition(after=new_val[key])
        elif old_val[key] == new_val[key]:
            ret[key] = NoChange()
        else:
            ret[key] = compare_any(old_val[key], new_val[key])
    
    return ret


OcsfT = TypeVar("OcsfT", bound=OcsfModel, covariant=True)
def create_diff(val: OcsfT) -> ChangedModel[OcsfT]:
    match val:
        case OcsfSchema():
            ret = DiffSchema()
        case OcsfEvent():
            ret = DiffEvent()
        case OcsfAttr():
            ret = DiffAttr()
        case _:
            raise ValueError("Unexpected model type")
    
    return cast(ChangedModel[OcsfT], ret)

def is_optional_dict(value: dict[Any, Any] | None, origin: type | UnionType, args: tuple[type, ...]) -> TypeGuard[dict[Any, Any] | None]:
    if isinstance(value, dict):
        return True
    if origin != Union or len(args) != 2:
        return False

    for arg in args:
        arg_origin = get_origin(arg)
        if arg is not NoneType and arg_origin is not dict:
            return False

    return True


def compare_any(old_val: T, new_val: T) -> Difference[T]:
    if isinstance(old_val, OcsfModel) and type(old_val) == type(new_val):
        ret = create_diff(old_val)

        for attr, value in get_type_hints(old_val).items():
            old_attr = getattr(old_val, attr)
            new_attr = getattr(new_val, attr)

            origin = get_origin(value)
            args = get_args(value)

            if is_optional_dict(old_attr, origin, args) and is_optional_dict(new_attr, origin, args):
                setattr(ret, attr, compare_dict(old_attr, new_attr))
            else:
                setattr(ret, attr, compare_any(old_attr, new_attr))
        
        return cast(Difference[T], ret)
    
    elif old_val == new_val:
        return NoChange()

    else:
        return Change(before=old_val, after=new_val)


if __name__ == "__main__":
    be1 = OcsfEvent(caption="Base Event", name="base", attributes={
        "size": OcsfAttr(caption="Size")
    })
    be2 = OcsfEvent(caption="Base", name="base", attributes={
        "size": OcsfAttr(caption="Sz")
    })

    new_e = OcsfEvent(caption="Shiny and new", name="newe")
    old_e = OcsfEvent(caption="Old and dirty", name="olde")
    same_e = OcsfEvent(caption="Same Event", name="samee", attributes={
        "height": OcsfAttr(caption="Height"),
        "width": OcsfAttr(caption="Width"),
    })
    changed_e1 = OcsfEvent(caption="Changed Event 1", name="changed", attributes={
        "speed": OcsfAttr(caption="Speed"),
        "power": OcsfAttr(caption="Power"),
        "mass": OcsfAttr(caption="Mass"),
    }, enum={"Lumens": OcsfAttr(caption="Lumens")})

    changed_e2 = OcsfEvent(caption="Changed Event 1", name="changed", attributes={
        "speed": OcsfAttr(caption="Speed"),
        "power": OcsfAttr(caption="Power (and more of it)"),
        "energy": OcsfAttr(caption="Energy"),
    })

    schema1 = OcsfSchema(version="0.1", base_event=be1, classes={
        "olde": old_e,
        "samee": same_e,
        "changede": changed_e1,
    })
    schema2 = OcsfSchema(version="0.2", base_event=be2, classes={
        "newe": new_e,
        "samee": same_e,
        "changede": changed_e2,
    })


    from pprint import pprint
    pprint(compare_any(schema1, schema2))