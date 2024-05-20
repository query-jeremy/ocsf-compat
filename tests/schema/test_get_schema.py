
import os
import pytest

from ocsf_tools.schema.model import OcsfSchema
from ocsf_tools.schema.http import OcsfServerClient
from ocsf_tools.schema.get_schema import get_schema


LOCATION = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(LOCATION, "../..", "schema_cache")


def test_get_schema_file():
    """Test fetching a schema from a file."""
    schema = get_schema(os.path.join(CACHE, "schema-1.1.0.json"))
    assert isinstance(schema, OcsfSchema)
    assert schema.version == "1.1.0"
    assert len(schema.classes) > 0
    assert len(schema.objects) > 0


def test_get_schema_version_cache():
    """Test fetching a schema by version from the cache."""
    schema = get_schema("1.1.0", OcsfServerClient(cache_dir=CACHE))
    assert isinstance(schema, OcsfSchema)
    assert schema.version == "1.1.0"
    assert len(schema.classes) > 0
    assert len(schema.objects) > 0


@pytest.mark.integration
def test_get_schema_version_server():
    """Test fetching a schema by version from the server."""
    schema = get_schema("1.1.0")
    assert isinstance(schema, OcsfSchema)
    assert schema.version == "1.1.0"
    assert len(schema.classes) > 0
    assert len(schema.objects) > 0