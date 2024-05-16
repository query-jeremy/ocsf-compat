import os
from ocsf_tools.schema import OcsfEvent, from_json

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
                "caption": "Status",
                "type": "int_t",
                "requirement": "required",
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
            "caption": "Timestamp",
            "requirement": "required",
            "description": "Event timestamp"
        }
    }
  
  }
}"""


def test_decode_str():
    schema = from_json(JSON_DATA)
    assert len(schema.classes) > 0
    assert "authentication" in schema.classes
    assert isinstance(schema.classes["authentication"], OcsfEvent)


def test_decode_file():
    json_str: str | None = None
    with open(SCHEMA_JSON, "r") as f:
        json_str = f.read()
    assert json_str is not None
    schema = from_json(json_str)

    assert len(schema.classes) > 0
    assert "authentication" in schema.classes
    assert isinstance(schema.classes["authentication"], OcsfEvent)
