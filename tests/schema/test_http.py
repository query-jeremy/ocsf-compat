
import pytest

from ocsf_tools.schema.http import OcsfServerClient


@pytest.mark.integration
def test_get_versions():
    client = OcsfServerClient()
    versions = client.get_versions()

    assert isinstance(versions, list)
    assert len(versions) > 0
    assert "1.0.0" in versions
    assert "1.1.0" in versions
    assert "1.2.0" in versions