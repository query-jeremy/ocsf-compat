"""Compare OCSF schemata.


"""

from typing import Any, Optional, TypeVar, Union, get_args, get_type_hints, get_origin, overload

from ocsf_schema.model import (
    OcsfName,
    OcsfSchema,
    OcsfEvent,
    OcsfObject,
    OcsfAttr,
    OcsfDeprecationInfo,
    OcsfModel,
    OcsfDictionary,
    OcsfCategories,
    OcsfInclude,
    OcsfProfile,
    OcsfExtension,
    OcsfVersion,
)
from ocsf_diff.model import (
    Difference,
    Addition,
    Removal,
    Change,
    NoChange,
    DiffSchema,
    DiffEvent,
    DiffObject,
    DiffAttr,
    DiffDeprecationInfo,
    DiffModel,
    DiffDictionary,
    DiffCategories,
    DiffInclude,
    DiffProfile,
    DiffExtension,
    DiffVersion,
)
from ocsf_diff.factory import create_diff

AnyT = TypeVar("AnyT")
def _compare_primitive(old: AnyT, new: AnyT) -> Difference[AnyT]:
    if old == new:
        return NoChange[AnyT]()
    # elif old is None:
    #    return Addition[AnyT](after=new)
    # elif new is None:
    #    return Removal[AnyT](before=old)
    else:
        return Change[AnyT](before=old, after=new)


_MODEL_TYPES = get_args(OcsfModel)

def _find_ocsf_type(t: type) -> type | None:
    if t in _MODEL_TYPES:
        return t

    t_origin = get_origin(t)
    if t_origin in (Union, dict):
        for arg in get_args(t):
            found = _find_ocsf_type(arg)
            if found is not None:
                return found

    return None

# @overload
# def compare(old: OcsfSchema, new: OcsfSchema) -> DiffSchema: ...

OcsfT = TypeVar("OcsfT", bound=OcsfModel)

def _compare_dict(old_val: Optional[dict[OcsfName, OcsfT]], new_val: Optional[dict[OcsfName, OcsfT]]) -> dict[OcsfName, Difference[OcsfT]]:
    diff_dict: dict[OcsfName, Difference[OcsfT]] = {}

    old_d = old_val if old_val is not None else {}
    new_d = new_val if new_val is not None else {}
    keys: set[OcsfName] = set(old_d.keys()) | set(new_d.keys())

    for key in keys:
        if key not in new_d:
            diff_dict[key] = Removal(before=old_d[key])
        elif key not in old_d:
            diff_dict[key] = Addition(after=new_d[key])
        elif old_d[key] == new_d[key]:
            diff_dict[key] = NoChange()
        elif isinstance(old_d[key], OcsfModel) and isinstance(
            new_d[key], OcsfModel
        ):
            diff_dict[key] = compare(old_d[key], new_d[key])
        else:
            diff_dict[key] = _compare_primitive(old_d[key], new_d[key])

    return diff_dict

def compare(old_model: OcsfT, new_model: OcsfT) -> Difference[OcsfT]:
    diff = create_diff(old_model)
    hints = get_type_hints(old_model)

    for attr, value in hints.items():
        old_val = getattr(old_model, attr)
        new_val = getattr(new_model, attr)
        ocsf_type = _find_ocsf_type(value)

        # Scenarios
        # 1. Two OCSF models (recurse)
        if isinstance(old_val, OcsfModel) and isinstance(new_val, OcsfModel):
            setattr(diff, attr, compare(old_val, new_val))
        
        # 2. One OCSF model, one None (optional) - Add/Remove
        elif isinstance(old_val, OcsfModel) or isinstance(new_val, OcsfModel):
            if old_val is None:
                setattr(diff, attr, Addition(after=new_val))
            elif new_val is None:
                setattr(diff, attr, Removal(before=old_val))
            else:
                raise ValueError(f"Unexpected union type for {attr}")

        # 3. dict[str, OcsfModel] or Optional[dict[str, OcsfModel]]
        elif ocsf_type is not None and (isinstance(old_val, dict) or isinstance(new_val, dict)):
            # We know that model.py doesn't have any properties that would cause
            # problems with the line below, so type checking is disabled. But
            # there's probably a way to enable it and get the desired result.
            setattr(diff, attr, _compare_dict(old_val, new_val)) # type: ignore

        # 4. everything else
        else:
            setattr(diff, attr, _compare_primitive(old_val, new_val))

    return diff