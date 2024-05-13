
from typing import TypeVar, get_type_hints, get_origin, cast

from type_hell.diff import DiffSchema, DiffEvent, DiffAttr, Difference, NoChange, Addition, Removal, Change
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


def compare_any(old_val: T, new_val: T) -> Difference[T]:
    if isinstance(old_val, OcsfModel) and type(old_val) == type(new_val):
        match old_val:
            case OcsfSchema():
                ret = DiffSchema()
            case OcsfEvent():
                ret = DiffEvent()
            case OcsfAttr():
                ret = DiffAttr()
            case _:
                raise ValueError("Unexpected model type")
        
        for attr, value in get_type_hints(old_val).items():
            old_attr = getattr(old_val, attr)
            new_attr = getattr(new_val, attr)

            origin = get_origin(value)
            if origin == dict:
                setattr(ret, attr, compare_dict(old_attr, new_attr))
            else:
                setattr(ret, attr, compare_any(old_attr, new_attr))
        
        return cast(Difference[T], ret)
    
    elif old_val == new_val:
        return NoChange[T]()

    else:
        return Change[T](before=old_val, after=new_val)


if __name__ == "__main__":
    be1 = OcsfEvent(caption="Base Event", name="base", attributes={
        "size": OcsfAttr(caption="Size")
    })
    be2 = OcsfEvent(caption="Base", name="base", attributes={
        "size": OcsfAttr(caption="Sz")
    })

    schema1 = OcsfSchema(version="0.1", base_event=be1)
    schema2 = OcsfSchema(version="0.2", base_event=be2)

    from pprint import pprint
    pprint(compare_any(schema1, schema2))