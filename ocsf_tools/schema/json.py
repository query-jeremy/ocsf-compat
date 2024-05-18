"""Transform OCSF schema to and from JSON in strings and files.

Examples:
```python
schema = from_json('{"version": "1.0.0", "classes": [], "objects": []}')
schema = from_file("schema.json")
```

"""

import json
from dataclasses import asdict
from typing import Any, cast

from dacite import from_dict

from .model import OcsfSchema

# Certain OCSF properties have special characters in their names.
_KEY_TRANSFORMS = {
    "@deprecated": "deprecated",
    "$include": "include",
}

_NAME_TRANSFORMS = {
    "deprecated": "@deprecated",
    "include": "$include",
}


def keys_to_names(d: dict[str, Any]) -> dict[str, Any]:
    """Transform OCSF property names in JSON to Python-friendly names."""
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
    """Transform Python-friendly names to OCSF property names in JSON."""
    for k, v in d.items():
        if k in _NAME_TRANSFORMS:
            d[_NAME_TRANSFORMS[k]] = d[k]
            del d[k]

        elif isinstance(k, dict):
            d[k] = names_to_keys(v)

    return d


def from_json(data: str) -> OcsfSchema:
    """Parse an OCSF schema from a JSON string."""
    return from_dict(OcsfSchema, keys_to_names(json.loads(data)))  # type: ignore


def to_dict(schema: OcsfSchema) -> dict[str, Any]:
    """Convert an OCSF schema to a dictionary."""
    return names_to_keys(asdict(schema))


def to_json(schema: OcsfSchema) -> str:
    """Convert an OCSF schema to a JSON string."""
    return json.dumps(to_dict(schema))


def from_file(path: str) -> OcsfSchema:
    """Parse an OCSF schema from a JSON file."""
    with open(path, "r") as f:
        return from_json(f.read())


def to_file(schema: OcsfSchema, path: str) -> None:
    """Write an OCSF schema to a JSON file."""
    with open(path, "w") as f:
        f.write(to_json(schema))
