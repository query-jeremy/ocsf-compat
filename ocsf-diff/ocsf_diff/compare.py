"""Compare OCSF schemata."""

from typing import (
    TypeVar,
    TypeGuard,
    Union,
    get_args,
    get_type_hints,
    get_origin,
    Any,
    cast,
)
from types import UnionType, NoneType

from ocsf_schema.model import OcsfModel
from ocsf_diff.model import (
    Difference,
    Addition,
    Removal,
    Change,
    NoChange,
)
from ocsf_diff.factory import create_diff


T = TypeVar("T")
K = TypeVar("K")


def compare_dict(old_val: dict[K, T] | None, new_val: dict[K, T] | None) -> dict[K, Difference[T]] | NoChange[T]:
    if old_val is None and new_val is None:
        return NoChange()

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
            ret[key] = compare(old_val[key], new_val[key])

    return ret


def is_optional_dict(
    value: dict[Any, Any] | None, origin: type | UnionType, args: tuple[type, ...]
) -> TypeGuard[dict[Any, Any] | None]:
    if isinstance(value, dict):
        return True
    if origin != Union or len(args) != 2:
        return False

    for arg in args:
        arg_origin = get_origin(arg)
        if arg is not NoneType and arg_origin is not dict:
            return False

    return True


def compare(old_val: T, new_val: T) -> Difference[T]:
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
                setattr(ret, attr, compare(old_attr, new_attr))

        return cast(Difference[T], ret)

    elif old_val == new_val:
        return NoChange()

    else:
        return Change(before=old_val, after=new_val)
