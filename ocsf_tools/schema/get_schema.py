from typing import Optional
from .model import OcsfSchema
from .json import from_file
from .http import OcsfServerClient


def get_schema(versionOrFile: Optional[str] = None, client: Optional[OcsfServerClient] = None) -> OcsfSchema:
    """Fetch a schema from a filename or version.

    This is a convenience function.

    Example:
        ```python
        schema = get_schema("1.1.0")
        schema = get_schema("ocsf-1.1.0.json")
        ```

    Args:
        versionOrFile: The name of an OCSF schema file or a valid semantic version number.

    Returns:
        The requested OcsfSchema.

    Raises:
        ValueError: If the version requested is not found on the server or
            if the requested version is invalid.
    """
    if versionOrFile is not None:
        try:
            return from_file(versionOrFile)
        except FileNotFoundError:
            pass

    if client is None:
        client = OcsfServerClient()

    return client.get_schema(versionOrFile)
