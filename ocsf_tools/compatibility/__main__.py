import tomllib
from argparse import ArgumentParser
from typing import cast
import logging
import sys

from ocsf_tools.schema import from_file, OcsfServerClient
from ocsf_tools.validation import Severity, ValidationFormatter, validate_severities
from ocsf_tools.compare import compare, ChangedSchema

from .validator import CompatibilityValidator

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

config = {
    "before": "1.0.0",
}

severities: dict[str, Severity] = {}

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

if args.config:
    conf = tomllib.load(args.config)

    if "before" in conf:
        config["before"] = conf["before"]
    if "after" in conf:
        config["after"] = conf["after"]
    if "cache" in conf:
        config["cache"] = conf["cache"]
    if "info" in conf:
        config["info"] = conf["info"]

    if "severity" in conf:
        sevs = conf["severity"]
        if isinstance(sevs, dict):
            severities |= cast(dict[str, Severity], sevs)

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

# TODO: import all relevant Finding classes or this will fail
validate_severities(severities)

if "before" not in config:
    print("Missing before schema file or version")
    exit(1)

if "after" not in config:
    print("Missing after schema file or version")
    exit(1)

client = OcsfServerClient(cache_dir=config.get("cache", None))

try:
    before = from_file(config["before"])
except FileNotFoundError:
    before = client.get_schema(config["before"])

try:
    after = from_file(config["after"])
except FileNotFoundError:
    after = client.get_schema(config["after"])

validator = CompatibilityValidator(cast(ChangedSchema, compare(before, after)), severities)
formatter = ValidationFormatter()
print(formatter.format(validator.validate()))
