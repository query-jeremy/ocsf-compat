"""Compare OCSF schemata."""

from typing import (
    Optional,
    TypeVar,
    Union,
    get_args,
    get_type_hints,
    get_origin,
    overload,
)

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
    OcsfEnumMember,
    OcsfDictionaryTypes,
)
from ocsf_diff.model import (
    Difference,
    Addition,
    Removal,
    Change,
    NoChange,
    OcsfComparable,
    COMPARABLE_TYPES,
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
    DiffEnumMember,
    DiffDictionaryTypes,
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


# TODO type signature for Union and other special forms
def _find_ocsf_type(t: type) -> type | None:
    if t in COMPARABLE_TYPES:
        return t

    t_origin = get_origin(t)
    if t_origin in (Union, dict):
        for arg in get_args(t):
            found = _find_ocsf_type(arg)
            if found is not None:
                return found

    return None


def _compare_dict(
    old_val: Optional[dict[OcsfName, OcsfComparable]],
    new_val: Optional[dict[OcsfName, OcsfComparable]],
) -> dict[OcsfName, Difference[OcsfComparable]]:
    diff_dict: dict[OcsfName, Difference[OcsfComparable]] = {}

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
        elif isinstance(old_d[key], OcsfModel) and isinstance(new_d[key], OcsfModel):
            diff_dict[key] = compare(old_d[key], new_d[key])
        else:
            diff_dict[key] = _compare_primitive(old_d[key], new_d[key])

    return diff_dict


@overload
def compare(old_model: OcsfAttr, new_model: OcsfAttr) -> DiffAttr: ...


@overload
def compare(old_model: OcsfSchema, new_model: OcsfSchema) -> DiffSchema: ...


@overload
def compare(old_model: OcsfEvent, new_model: OcsfEvent) -> DiffEvent: ...


@overload
def compare(old_model: OcsfObject, new_model: OcsfObject) -> DiffObject: ...


@overload
def compare(
    old_model: OcsfDeprecationInfo, new_model: OcsfDeprecationInfo
) -> DiffDeprecationInfo: ...


@overload
def compare(old_model: OcsfDictionary, new_model: OcsfDictionary) -> DiffDictionary: ...


@overload
def compare(old_model: OcsfCategories, new_model: OcsfCategories) -> DiffCategories: ...


@overload
def compare(old_model: OcsfInclude, new_model: OcsfInclude) -> DiffInclude: ...


@overload
def compare(old_model: OcsfProfile, new_model: OcsfProfile) -> DiffProfile: ...


@overload
def compare(old_model: OcsfExtension, new_model: OcsfExtension) -> DiffExtension: ...


@overload
def compare(old_model: OcsfVersion, new_model: OcsfVersion) -> DiffVersion: ...


@overload
def compare(old_model: OcsfEnumMember, new_model: OcsfEnumMember) -> DiffEnumMember: ...

@overload
def compare(old_model: OcsfDictionaryTypes, new_model: OcsfDictionaryTypes) -> DiffDictionaryTypes: ...


def compare(old_model: OcsfComparable, new_model: OcsfComparable) -> DiffModel:
    diff = create_diff(old_model)
    hints = get_type_hints(old_model)

    for attr, value in hints.items():
        old_val = getattr(old_model, attr)
        new_val = getattr(new_model, attr)
        ocsf_type = _find_ocsf_type(value)

        # Scenarios
        # 1. Two OCSF models (recurse)
        if isinstance(old_val, OcsfModel) and isinstance(new_val, OcsfModel):
            assert type(old_val) == type(new_val)
            assert type(old_val) in COMPARABLE_TYPES
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
        elif ocsf_type is not None and (
            isinstance(old_val, dict) or isinstance(new_val, dict)
        ):
            # We know that model.py doesn't have any properties that would cause
            # problems with the line below, so type checking is disabled. But
            # there's probably a way to enable it and get the desired result.
            setattr(diff, attr, _compare_dict(old_val, new_val))  # type: ignore

        # 4. everything else
        else:
            setattr(diff, attr, _compare_primitive(old_val, new_val))

    return diff
