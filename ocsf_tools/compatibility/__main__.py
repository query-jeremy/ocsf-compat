"""
This module is the entry point for the compatibility tool.

Most of what you'll find here is glue code to combine configuration from CLI
arguments and an optional TOML file. Skip to the bottom to see a validator
initialized and run.

This module uses `get_schema` to load the schemas to be compared from either a
local file or, if a version number is used, the OCSF server (or a cached copy).

Valid TOML configuration options are:
- before: The path or version of the "before" schema.
- after: The path or version of the "after" schema.
- cache: The path to the schema cache directory.
- severity: A dictionary of finding names to severities. Severity may be one of
  "info", "warning", "error", or "fatal".

See example.toml for an example configuration file.

Valid command line arguments are:
```
options:
  -h, --help            show this help message and exit
  --before BEFORE, -b BEFORE
                        Path to the schema file before the change
  --after AFTER, -a AFTER
                        Path to the schema file before the change
  --cache CACHE         Path to the schema cache directory
  --config CONFIG       Path to the config.toml file
  --info [INFO ...]     A finding to assign an info severity to
  --warning [WARNING ...]
                        A finding to assign an warning severity to
  --error [ERROR ...]   A finding to assign an error severity to
  --fatal [FATAL ...]   A finding to assign an fatal severity to
```

Examples:

Validate a schema defined in a file is compatible with 1.0.0 from the OCSF server:

    $ python -m ocsf_tools.compatibility --after ./schema.json --before 1.0.0


Validate two schema versions available from the OCSF server with a local cache:

    $ python -m ocsf_tools.compatibility --before 1.0.0 --after 1.1.0 --cache ./schema_cache 

Validate schemata using a configuration file: 

    $ python -m ocsf_tools.compatibility --config ./config.toml

Validate schemata but don't worry about removed enum members:

    $ python -m ocsf_tools.compatibility --config ./config.toml --info RemovedEnumMember

"""

import tomllib
from argparse import ArgumentParser
from typing import cast

from ocsf_tools.schema import get_schema, OcsfServerClient
from ocsf_tools.validation import Severity, ColoringValidationFormatter, validate_severities, count_severity
from ocsf_tools.compare import compare, ChangedSchema

from .validator import CompatibilityValidator


# Various modules use logging. Configure as you see fit.
# import logging
# import sys
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# Default configuration
config = {
    "before": "1.0.0",
}

# Default finding names x severities
severities: dict[str, Severity] = {}

# Configure parser
parser = ArgumentParser(description="Validate compatibility between two OCSF schemas")
parser.add_argument("--before", "-b", help="Path to the schema file before the change")
parser.add_argument("--after", "-a", help="Path to the schema file before the change")
parser.add_argument("--cache", help="Path to the schema cache directory")
parser.add_argument("--config", help="Path to the config.toml file")
parser.add_argument("--info", nargs="*", action="append", help="A finding to assign an info severity to")
parser.add_argument("--warning", nargs="*", action="append", help="A finding to assign an warning severity to")
parser.add_argument("--error", nargs="*", action="append", help="A finding to assign an error severity to")
parser.add_argument("--fatal", nargs="*", action="append", help="A finding to assign an fatal severity to")

args = parser.parse_args()


# Read configuration from file
if args.config:
    with open(args.config, "rb") as f:
        conf = tomllib.load(f)

        if "before" in conf:
            config["before"] = conf["before"]
        if "after" in conf:
            config["after"] = conf["after"]
        if "cache" in conf:
            config["cache"] = conf["cache"]
        if "severity" in conf:
            sevs = conf["severity"]
            if isinstance(sevs, dict):
                severities |= cast(dict[str, Severity], sevs)

# Override configuration from command line arguments
if args.before:
    config["before"] = args.before

if args.after:
    config["after"] = args.after

if args.cache:
    config["cache"] = args.cache

if args.info:
    for finding in args.info:
        for f in finding:
            severities[f] = Severity.INFO

if args.warning:
    for finding in args.warning:
        for f in finding:
            severities[f] = Severity.WARNING

if args.error:
    for finding in args.error:
        for f in finding:
            severities[f] = Severity.ERROR

if args.fatal:
    for finding in args.fatal:
        for f in finding:
            severities[f] = Severity.FATAL

# Check severity names
validate_severities(severities)


# Enforce that before and after are present
if "before" not in config:
    print("Missing before schema file or version")
    exit(1)

if "after" not in config:
    print("Missing after schema file or version")
    exit(1)

# Load the schemas
client = OcsfServerClient(cache_dir=config.get("cache", None))
before = get_schema(config["before"], client)
after = get_schema(config["after"], client)

# Configure a validator and run it
validator = CompatibilityValidator(cast(ChangedSchema, compare(before, after)), severities)
formatter = ColoringValidationFormatter()
results = validator.validate()

# Show the results
print(formatter.format(results))

# Exit with an error code if there are any errors or fatal findings
if count_severity(results, Severity.ERROR) > 0 or count_severity(results, Severity.FATAL) > 0:
    exit(2)
