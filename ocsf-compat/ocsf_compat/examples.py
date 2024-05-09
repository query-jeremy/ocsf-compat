"""OCSF Backwards Compatibility Validator PoC

This demonstrates how the APIs the sibling ocsf-schema and ocsf-diff packages
can be used to validate backwards compatibility between two OCSF schemata.

There are three checks:
 1. Check for removed (or renamed) events
 2. Check for changed requirements
 3. Check for changed types

A production-grade validator would accept arguments from a CLI, configuration
file, or environment variables. The structure of its checks should be reusable,
its output standardized, and its methods constrained by the type system. But
this should get the point across.
"""
import os

from ocsf_schema import from_file
from ocsf_diff import compare, Change, Removal, DiffEvent, DiffAttr


# TODO find schema files from configuration or CLI arguments
LOCATION = os.path.dirname(os.path.abspath(__file__))
OLD_JSON = os.path.join(LOCATION, "../tests/schema-1.0.0.json")
NEW_JSON = os.path.join(LOCATION, "../tests/schema-1.3.0-dev.json")


with open(OLD_JSON, "r") as f:
    old_schema = from_file(f.read())

with open(NEW_JSON, "r") as f: 
    new_schema = from_file(f.read())

assert old_schema is not None
assert new_schema is not None

diff = compare(old_schema, new_schema)


# Example 1: Check for removed (or renamed) events
for name, event in diff.classes.items():
    match event:
        case Removal():
            print(f"ERROR: event {name} was removed")
            # Here we could look for events in the new schema with the said UID
            # or Caption as the removed event had in the old schema to detect a
            # rename for more helpful error messages.
        case _:
            continue


# Example 2: Check for changed requirements
for name, event in diff.classes.items():
    if isinstance(event, DiffEvent):
        for attr_name, attr in event.attributes.items():
            if isinstance(attr, DiffAttr):
                if isinstance(attr.requirement, Change) and attr.requirement.after == "required":
                    print(f"ERROR: {name}.{attr_name} changed from {attr.requirement.before} to required")
                    # There's no need to check requirement.before – if the old
                    # and new value were the same, it wouldn't be a Change. And
                    # changing from anything to required is breaking.


# Example 3: Check for changed types
for name, event in diff.classes.items():
    if isinstance(event, DiffEvent):
        for attr_name, attr in event.attributes.items():
            if isinstance(attr, DiffAttr):
                if isinstance(attr.type, Change):
                    print(f"ERROR: {name}.{attr_name} changed from {attr.type.before} to {attr.type.after}")
                    # Any change of an attribute type could be a bad thing.
