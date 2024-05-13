"""Compare OCSF schemata."""

from types import UnionType
from typing import (
    TypeVar,
    TypeGuard,
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
    OcsfCategory,
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
    OcsfComparableU,
    DiffModel,
    COMPARABLE_TYPES,
    DiffSchema,
    DiffEvent,
    DiffObject,
    DiffAttr,
    DiffCategory,
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


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfDictionaryTypes],
    new_val: dict[OcsfName, OcsfDictionaryTypes],
) -> dict[OcsfName, Difference[OcsfDictionaryTypes]]: ...


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfAttr],
    new_val: dict[OcsfName, OcsfAttr],
) -> dict[OcsfName, Difference[OcsfAttr]]: ...


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfSchema],
    new_val: dict[OcsfName, OcsfSchema],
) -> dict[OcsfName, Difference[OcsfSchema]]: ...


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfEvent],
    new_val: dict[OcsfName, OcsfEvent],
) -> dict[OcsfName, Difference[OcsfEvent]]: ...


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfObject],
    new_val: dict[OcsfName, OcsfObject],
) -> dict[OcsfName, Difference[OcsfObject]]: ...


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfDeprecationInfo],
    new_val: dict[OcsfName, OcsfDeprecationInfo],
) -> dict[OcsfName, Difference[OcsfDeprecationInfo]]: ...


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfDictionary],
    new_val: dict[OcsfName, OcsfDictionary],
) -> dict[OcsfName, Difference[OcsfDictionary]]: ...


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfCategories],
    new_val: dict[OcsfName, OcsfCategories],
) -> dict[OcsfName, Difference[OcsfCategories]]: ...


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfInclude],
    new_val: dict[OcsfName, OcsfInclude],
) -> dict[OcsfName, Difference[OcsfInclude]]: ...


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfProfile],
    new_val: dict[OcsfName, OcsfProfile],
) -> dict[OcsfName, Difference[OcsfProfile]]: ...


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfExtension],
    new_val: dict[OcsfName, OcsfExtension],
) -> dict[OcsfName, Difference[OcsfExtension]]: ...


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfVersion],
    new_val: dict[OcsfName, OcsfVersion],
) -> dict[OcsfName, Difference[OcsfVersion]]: ...


@overload
def _compare_dict(
    old_val: dict[OcsfName, OcsfEnumMember],
    new_val: dict[OcsfName, OcsfEnumMember],
) -> dict[OcsfName, Difference[OcsfEnumMember]]: ...


def _compare_dict(
    old_val: dict[OcsfName, OcsfComparable],
    new_val: dict[OcsfName, OcsfComparable],
) -> dict[OcsfName, Difference[OcsfComparable]]:
    diff_dict: dict[OcsfName, Difference[OcsfComparable]] = {}

    keys: set[OcsfName] = set(old_val.keys()) | set(new_val.keys())

    for key in keys:
        if key not in new_val:
            diff_dict[key] = Removal(before=old_val[key])
        elif key not in old_val:
            diff_dict[key] = Addition(after=new_val[key])
        elif old_val[key] == new_val[key]:
            diff_dict[key] = NoChange()
        elif isinstance(old_val[key], OcsfComparableU) and isinstance(
            new_val[key], OcsfComparableU
        ):
            diff_dict[key] = compare(old_val[key], new_val[key])
        else:
            diff_dict[key] = _compare_primitive(old_val[key], new_val[key])

    return diff_dict

"""
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
def compare(old_model: OcsfCategory, new_model: OcsfCategory) -> DiffCategory: ...

@overload
def compare(old_model: OcsfInclude, new_model: OcsfInclude) -> DiffInclude: ...


@overload
def compare(old_model: OcsfProfile, new_model: OcsfProfile) -> DiffProfile: ...


@overload
def compare(old_model: OcsfExtension, new_model: OcsfExtension) -> DiffExtension: ...


@overload
def compare(old_model: OcsfVersion, new_model: OcsfVersion) -> DiffVersion: ...


@overload
def compare(
    old_model: OcsfDictionaryTypes, new_model: OcsfDictionaryTypes
) -> DiffDictionaryTypes: ...


@overload
def compare(old_model: OcsfEnumMember, new_model: OcsfEnumMember) -> DiffEnumMember: ...
"""

CompT = TypeVar("CompT", bound=OcsfModel)

def _comparable_models(models: tuple[OcsfModel, OcsfModel]) -> TypeGuard[tuple[OcsfModel, OcsfModel]]:
    return type(models[0]) == type(models[1]) # and isinstance(models[0], OcsfModel)

def compare(
    old_model: CompT, new_model: CompT 
) -> ChangedModel[CompT]:
    diff: ChangedModel[CompT] = create_diff(old_model)
    hints = get_type_hints(old_model)

    for attr, value in hints.items():
        old_val = getattr(old_model, attr)
        new_val = getattr(new_model, attr)
        ocsf_type = _find_ocsf_type(value)

        # Scenarios
        # 1. Two OCSF models (recurse)
        if _comparable_models((old_val, new_val)):#isinstance(old_val, OcsfModel) and isinstance(new_val, OcsfModel) and type(old_val) == type(new_val):
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

            # TODO check for optional dict
            setattr(
                diff,
                attr,
                _compare_dict(
                    old_val if old_val is not None else {},
                    new_val if new_val is not None else {},
                ),
            )  # type: ignore

        # 4. everything else
        else:
            setattr(diff, attr, _compare_primitive(old_val, new_val))

    return diff
