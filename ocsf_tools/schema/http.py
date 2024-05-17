"""
A simple caching HTTP client for fetching OCSF schemas from the server.

Example:

```python
from ocsf_tools.schema.http import OcsfServerClient
schema = OcsfServerClient().get_schema("1.0.0")
```

"""

import logging
import json

from urllib.request import urlopen
from urllib.parse import urljoin
from typing import Optional, cast
from semver import Version
from pathlib import Path

from .model import OcsfSchema
from .json import from_json, from_file, to_file

LOG = logging.getLogger(__name__)


def _is_semver(version: str) -> bool:
    try:
        Version.parse(version)
        return True
    except ValueError:
        return False


class OcsfServerClient:
    def __init__(self, base_url: str = "https://schema.ocsf.io", cache_dir: Optional[str | Path] = None):
        self._base_url = base_url
        if cache_dir is not None and not isinstance(cache_dir, Path):
            self._cache_dir = Path(cache_dir)
        else:
            self._cache_dir = cache_dir

    def get_versions(self) -> list[str]:
        url = urljoin(self._base_url, "api/versions")
        data = json.loads(urlopen(url).read())

        if not isinstance(data, dict) or "versions" not in data or not isinstance(data["versions"], list):
            raise ValueError("Invalid response from server")

        versions: list[dict[str, str]] = cast(list[dict[str, str]], data["versions"])
        result: list[str] = []
        for version in versions:
            if "version" not in version:
                LOG.warning(f"Invalid version in response from {url}: {version}")
            else:
                result.append(version["version"])

        return result

    def get_schema(self, version: Optional[str] = None) -> OcsfSchema:
        if version is not None:
            if not _is_semver(version):
                raise ValueError(f"Invalid version: {version}")

            if self._cache_dir is not None:
                if not self._cache_dir.exists():
                    LOG.debug(f"Creating cache directory: {self._cache_dir}")
                    self._cache_dir.mkdir(parents=True, exist_ok=True)

                file = self._cache_dir / f"schema-{version}.json"
                if file.exists():
                    LOG.info(f"Reading schema from cache: {file}")
                    return from_file(str(file))

            if version not in self.get_versions():
                raise ValueError(f"Version {version} not found on server")

        schema = self._fetch_schema(version)

        if self._cache_dir is not None:
            dest = str(self._cache_dir / f"schema-{schema.version}.json")
            LOG.debug(f"Caching schema to {dest}")
            to_file(schema, dest)

        return schema

    def _fetch_schema(self, version: Optional[str] = None) -> OcsfSchema:
        if version is not None:
            url = urljoin(self._base_url, f"{version}/")
        else:
            url = self._base_url

        url = urljoin(url, "export/schema")

        LOG.debug(f"Fetching schema from {url} (version {version})")
        json_str = urlopen(url).read()
        return from_json(json_str)


def from_http(version: Optional[str] = None) -> OcsfSchema:
    return OcsfServerClient().get_schema(version)
