# OCSF Schema Tools
Tools for working with the OCSF schema in Python.

## About
This project began with two goals:
1. Provide the OCSF community with a validator that tests for breaking changes in `ocsf-schema` PRs.
2. Begin to provide the OCSF community with more composable tools and libraries to make OCSF more "hackable."

The project targets Python 3.11 for a balance of capability and availability, is divided into discrete packages.

### The Schema Package
The `ocsf_tools.schema` package contains Python data classes that represent an OCSF schema as compiled and exported by the OCSF server's `export/schema` endpoint.

It also includes utilities to parse the schema from a JSON string or file, as well as a lightweight HTTP client that can retrieve a version of the schema over HTTP and cache it on the local filesystem.

### The Compare Package
The `ocsf_tools.compare` package compares two versions of the OCSF schema and
generates a type safe difference. Its aim is to make schema comparisons easy to
work with.

This package grew out of a library used internally at [Query](https://query.ai). The original is used extensively to manage upgrading Query's data model to newer versions of OCSF, as well as to build adapters between different OCSF flavors (like AWS Security Lake on rc2 and Query on 1.1). 

There is a very simple `__main__` implementation to demonstrate the comparison. You can use it as follows:

```sh
$ poetry run python -m ocsf_tools.compare 1.0.0 1.2.0
```

### The Validation Package 
The `ocsf_tools.validation` package provides a lightweight framework for
validators. It was inspired by the needs of `ocsf-validator`, which may be
ported to this framework in the future.

### The Compatibility Package
The `ocsf_tools.compatibility` package uses the other packages to provide a
validator that compares two OCSF schema and looks for breaking changes as
defined in the OCSF FAQ.

The compatibility validator can be run as follows:
```sh
$ poetry run python -m ocsf_tools.compatibility --before 1.0.0 --after 1.2.0 --cache ./cache
```

## Getting Started

### PyPI
The easiest way to install `ocsf-tools` is from PyPI using `pip` or `poetry`:
**NOTE**: Not actually published to PyPI yet.
```sh
$ pip install ocsf-tools
```

### From Source
If you want to work with the source, the recommended installation is with `asdf` and `poetry`.

```sh
$ asdf install
$ poetry install
```

## Contributing
This project uses `ruff` for formatting and linting, `pyright` for type checking, and `pytest` as its test runner.

Before submitting a PR, make sure you've run following:
```sh
$ poetry run ruff format
$ poetry run ruff check
$ poetry run pyright
$ poetry run pytest
```

### Type Checking
With great effort, this library passes pyright's strict mode type checking. Keep
it that way!

There is one cast used from the concrete `ChangedModel` types (`ChangedSchema`,
`ChangedAttr`, etc.) in the compare package to the generic type. For the life of
me, I can't figure it out. I blame pyright but it's probably my own fault.

### Tests

Running unit tests:
```sh
$ poetry run pytest -m "not integration"
```

Running integration tests:
```sh
$ poetry run pytest -m integration
```
**NOTE**: Some of the integration tests require an OCSF server instance, and are
*using the public instance at [https://schema.ocsf.io](https://schema.ocsf.io).
*This should probably use a local instance of the OCSF server instead.