from typing import Any, get_args, get_type_hints, get_origin, get_args

from ocsf_schema.model import *
from ocsf_diff.model import *


def _class_name(cls: type) -> str:
    # TODO delete this unused function
    # str(cls) will be something like:
    #   "<class 'ocsf_schema.OcsfSchema'>"
    return str(cls).split(".")[-1][:-2]


def _compare(old: Any, new: Any) -> Difference:
    if old == new:
        return None
    elif old is None:
        return Addition()
    elif new is None:
        return Removal()
    else:
        return Change(before=old, after=new)


def _create_diff(model: OcsfModel) -> DiffModel:
    match model:
        case OcsfSchema():
            return DiffSchema()
        case OcsfEvent():
            return DiffEvent()
        case OcsfObject():
            return DiffObject()
        case OcsfAttr():
            return DiffAttr()
        case OcsfDeprecationInfo():
            return DiffDeprecationInfo()
        case _:
            raise ValueError("Unrecognized model type")


def compare(old_model: OcsfModel, new_model: OcsfModel) -> DiffModel:
    diff = _create_diff(old_model)

    for k, v in get_type_hints(old_model).items():
        old_val = getattr(old_model, k)
        new_val = getattr(new_model, k)
        origin = get_origin(v)
        args = get_args(v)

        if isinstance(old_val, OcsfModel):
            setattr(diff, k, compare(old_val, new_val))

        elif origin is dict:
            if args[-1] in get_args(OcsfModel):
                diff_dict: dict[OcsfName, DiffModel] = {}

                keys = set(old_val.keys()) | set(new_val.keys())
                for key in keys:
                    if key not in new_val:
                        diff_dict[key] = Removal()
                    elif key not in old_val:
                        diff_dict[key] = Addition()
                    elif old_val[key] == new_val[key]:
                        diff_dict[key] = None
                    else:
                        diff_dict[key] = compare(old_val[key], new_val[key])

                setattr(diff, k, diff_dict)

        # elif origin is list:
        #    I'm fairly certain we don't need special handling for lists.

        else:
            setattr(diff, k, _compare(old_val, new_val))

    return diff


if __name__ == "__main__":
    # TODO - Remove this rubbish after writing unit tests

    from ocsf_schema import decode
    import os

    LOCATION = os.path.dirname(os.path.abspath(__file__))
    OLD_JSON = os.path.join(LOCATION, "../tests/schema-1.0.0.json")
    NEW_JSON = os.path.join(LOCATION, "../tests/schema-1.3.0-dev.json")

    old_schema: OcsfSchema
    new_schema: OcsfSchema

    with open(OLD_JSON, "r") as f:
        old_schema = decode(f.read())

    with open(NEW_JSON, "r") as f:
        new_schema = decode(f.read())

    assert old_schema is not None
    assert new_schema is not None

    diff = compare(old_schema, new_schema)
    from pprint import pprint

    pprint(diff)
