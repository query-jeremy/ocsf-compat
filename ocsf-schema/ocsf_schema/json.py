import json
from dataclasses import asdict
from typing import Any, cast

from dacite import from_dict

from ocsf_schema.model import OcsfSchema


_KEY_TRANSFORMS = {
    "@deprecated": "deprecated",
    "$include": "include",
}

_NAME_TRANSFORMS = {
    "deprecated": "@deprecated",
    "include": "$include",
}


def keys_to_names(d: dict[str, Any]) -> dict[str, Any]:
    ops: list[tuple[str, str]] = []

    for k, v in d.items():
        if k in _KEY_TRANSFORMS:
            ops.append((k, _KEY_TRANSFORMS[k]))

        elif isinstance(v, dict):
            d[k] = keys_to_names(cast(dict[str, Any], v))

    for op in ops:
        d[op[1]] = d[op[0]]
        del d[op[0]]

    return d


def names_to_keys(d: dict[str, Any]) -> dict[str, Any]:
    for k, v in d.items():
        if k in _NAME_TRANSFORMS:
            d[_NAME_TRANSFORMS[k]] = d[k]
            del d[k]

        elif isinstance(k, dict):
            d[k] = names_to_keys(v)

    return d


def decode(data: str) -> OcsfSchema:
    return from_dict(OcsfSchema, keys_to_names(json.loads(data)))


def encode(schema: OcsfSchema) -> str:
    return json.dumps(names_to_keys(asdict(schema)))
