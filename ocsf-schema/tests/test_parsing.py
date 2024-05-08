import os
import json
from ocsf_schema import OcsfSchema, OcsfEvent, decode

LOCATION = os.path.dirname(os.path.abspath(__file__))
SCHEMA_JSON = os.path.join(LOCATION, "schema.json")

JSON_DATA = """{
  "version": "1.0",
  "classes": {
    "authentication": {
        "name": "authentication",
        "description": "An authentication attempt",
        "category": "iam",
        "caption": "Authentication",
        "attributes": {
            "status": {
                "type": "int_t",
                "description": "Auth status"
            }
        }
    }
  },
  "objects": {
  
  },
  "types": {

  },
  "base_event": {
    "name": "base_event",
    "description": "Base event",
    "category": "base",
    "caption": "Base",
    "attributes": {
        "timestamp": {
            "type": "int_t",
            "description": "Event timestamp"
        }
    }
  
  }
}"""


def test_decode_str():
    schema = decode(JSON_DATA)
    assert len(schema.classes) > 0
    assert "authentication" in schema.classes
    assert isinstance(schema.classes["authentication"], OcsfEvent)


def test_decode_file():
    json_str: str | None = None
    with open(SCHEMA_JSON, "r") as f:
        json_str = f.read()
    assert json_str is not None
    schema = decode(json_str)

    assert len(schema.classes) > 0
    assert "authentication" in schema.classes
    assert isinstance(schema.classes["authentication"], OcsfEvent)