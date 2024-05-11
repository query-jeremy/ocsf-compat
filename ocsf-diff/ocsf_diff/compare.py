"""Compare OCSF schemata."""

from types import UnionType
from typing import (
    TypeVar,
    Any,
    TypeGuard,
    Union,
    Optional,
    get_args,
    cast,
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
    ChangedModel,
    OcsfComparable,
    COMPARABLE_TYPES,
    DiffSchema,
    DiffEvent,
    DiffObject,
    DiffAttr,
    DiffDeprecationInfo,
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


def _find_ocsf_type(t: type | UnionType) -> type | None:
    if not isinstance(t, UnionType) and t in COMPARABLE_TYPES:
        return t

    t_origin = get_origin(t)
    if t_origin in (Union, dict):
        for arg in get_args(t):
            found = _find_ocsf_type(arg)
            if found is not None:
                return found

    return None


def _is_comparable_ocsf(val: OcsfModel) -> TypeGuard[OcsfComparable]:
    return type(val) in COMPARABLE_TYPES

def _is_comparable_ocsf_pair(
    old_val: OcsfComparable, new_val: OcsfComparable,
) -> TypeGuard[OcsfComparable]:
    t1 = type(old_val)
    t2 = type(new_val)

    return _find_ocsf_type(t1) is not None and _find_ocsf_type(t2) is not None and t1 == t2

def _dict_type(val: dict[Any, Any]) -> tuple[set[type], set[type]]:
    types: tuple[set[type], set[type]] = (set(), set())

    for k, v in val.items():
        types[0].add(type(k))
        types[1].add(type(v))

    return types

def _dict_args(val: dict[Any, Any]) -> tuple[type, type]:
    dt = _dict_type(val)
    if len(dt[0]) > 1 or len(dt[1]) > 1:
        raise ValueError(f"Non-homogeneous dict {dt[0]}: {dt[1]}")
    return (dt[0].pop(), dt[1].pop())


def _is_comparable_ocsf_dict(val: dict[OcsfName, OcsfComparable] | Any, args: Optional[tuple[type, type]] = None) -> TypeGuard[dict[OcsfName, OcsfComparable]]:
    if not isinstance(val, dict):
        return False
    if args is None:
        args = _dict_args(cast(dict[Any, Any], val))
    return args[1] in COMPARABLE_TYPES

def _is_comparable_ocsf_dict_pair(val: tuple[dict[OcsfName, OcsfComparable] | Any, dict[OcsfName, OcsfComparable] | Any], args: Optional[tuple[type, type]] = None) -> TypeGuard[dict[OcsfName, OcsfComparable]]:
    if not isinstance(val[0], dict) or not isinstance(val[1], dict):
        return False
    if args is not None:
        return args[1] in COMPARABLE_TYPES
    else:
        t1 = _dict_args(cast(dict[Any, Any], val[0]))[1]
        t2 = _dict_args(cast(dict[Any, Any], val[1]))[1]
        return t1 == t2 and t1 in COMPARABLE_TYPES


def compare_primitive(old: AnyT, new: AnyT) -> Difference[AnyT]:
    if old == new:
        return NoChange[AnyT]()
    else:
        return Change[AnyT](before=old, after=new)

def add_dict_items(new_val: dict[OcsfName, OcsfComparable]) -> dict[OcsfName, Difference[OcsfComparable]]:
    return {k: Addition(after=v) for k, v in new_val.items()}

def remove_dict_items(old_val: dict[OcsfName, OcsfComparable]) -> dict[OcsfName, Difference[OcsfComparable]]:
    return {k: Removal(before=v) for k, v in old_val.items()}


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfSchema], new_dict: dict[OcsfName, OcsfSchema]) -> dict[OcsfName, Difference[OcsfSchema]]: ...


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfEvent], new_dict: dict[OcsfName, OcsfEvent]) -> dict[OcsfName, Difference[OcsfEvent]]: ...


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfObject], new_dict: dict[OcsfName, OcsfObject]) -> dict[OcsfName, Difference[OcsfObject]]: ...


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfAttr], new_dict: dict[OcsfName, OcsfAttr]) -> dict[OcsfName, Difference[OcsfAttr]]: ...


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfDeprecationInfo], new_dict: dict[OcsfName, OcsfDeprecationInfo]) -> dict[OcsfName, Difference[OcsfDeprecationInfo]]: ...


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfDictionary], new_dict: dict[OcsfName, OcsfDictionary]) -> dict[OcsfName, Difference[OcsfDictionary]]: ...


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfDictionaryTypes], new_dict: dict[OcsfName, OcsfDictionaryTypes]) -> dict[OcsfName, Difference[OcsfDictionaryTypes]]: ...


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfCategories], new_dict: dict[OcsfName, OcsfCategories]) -> dict[OcsfName, Difference[OcsfCategories]]: ...


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfInclude], new_dict: dict[OcsfName, OcsfInclude]) -> dict[OcsfName, Difference[OcsfInclude]]: ...


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfProfile], new_dict: dict[OcsfName, OcsfProfile]) -> dict[OcsfName, Difference[OcsfProfile]]: ...


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfExtension], new_dict: dict[OcsfName, OcsfExtension]) -> dict[OcsfName, Difference[OcsfExtension]]: ...


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfVersion], new_dict: dict[OcsfName, OcsfVersion]) -> dict[OcsfName, Difference[OcsfVersion]]: ...


@overload
def compare_dicts(old_dict: dict[OcsfName, OcsfEnumMember], new_dict: dict[OcsfName, OcsfEnumMember]) -> dict[OcsfName, Difference[OcsfEnumMember]]: ...

def compare_dicts(old_dict: dict[OcsfName, OcsfComparable], new_dict: dict[OcsfName, OcsfComparable]) -> dict[OcsfName, Difference[OcsfComparable]]:
    diff_dict: dict[OcsfName, Difference[OcsfComparable]]  = {}
    keys: set[OcsfName] = set(old_dict.keys()) | set(new_dict.keys())

    for key in keys:
        if key not in new_dict and _is_comparable_ocsf(old_dict[key]):
            diff_dict[key] = Removal(before=old_dict[key])
        elif key not in old_dict and _is_comparable_ocsf(new_dict[key]):
            diff_dict[key] = Addition(after=new_dict[key])
        else:
            old_val = old_dict[key]
            new_val = new_dict[key]
            if old_val == new_val:
                diff_dict[key] = NoChange()
            elif _is_comparable_ocsf_pair(old_val, new_val):
                diff_dict[key] = compare(old_val, new_val)
            else:
                raise ValueError("what's this?!?")

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
def compare(old_model: OcsfDeprecationInfo, new_model: OcsfDeprecationInfo) -> DiffDeprecationInfo: ...


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
def compare(old_model: OcsfDictionaryTypes, new_model: OcsfDictionaryTypes) -> DiffDictionaryTypes: ...


@overload
def compare(old_model: OcsfEnumMember, new_model: OcsfEnumMember) -> DiffEnumMember: ...

def compare(old_model: OcsfComparable, new_model: OcsfComparable) -> ChangedModel[OcsfComparable]:
    diff = create_diff(old_model)
    hints = get_type_hints(old_model)

    for attr, value in hints.items():
        old_val = getattr(old_model, attr)
        new_val = getattr(new_model, attr)
        args = get_args(value)

        # Scenarios
        # 1. Two OCSF models (recurse)
        if _is_comparable_ocsf_pair(old_val, new_val):
            setattr(diff, attr, compare(old_val, new_val))

        # 2. One OCSF model, one None (optional) - Add/Remove
        elif isinstance(old_val, OcsfModel) or isinstance(new_val, OcsfModel):
            if old_val is None:
                setattr(diff, attr, Addition(after=new_val))
            elif new_val is None:
                setattr(diff, attr, Removal(before=old_val))
            else:
                raise ValueError(f"Unexpected union type for {attr}")

        # 3. Two dict[OcsfName, OcsfComparable]
        elif _is_comparable_ocsf_dict_pair((old_val, new_val), args):
            setattr(diff, attr, compare_dicts(old_val, new_val))

        # 4. dict[OcsfName, OcsfComparable] and None
        elif _is_comparable_ocsf_dict(old_val, args) and new_val is None:
            setattr(diff, attr, remove_dict_items(old_val))

        # 5. None and dict[OcsfName, OcsfComparable]
        elif _is_comparable_ocsf_dict(new_val, args) and old_val is None:
            setattr(diff, attr, add_dict_items(new_val))

        # 6. everything else
        else:
            setattr(diff, attr, compare_primitive(old_val, new_val))

    return diff
