#!/usr/bin/env bash

poetry run ruff format
if [ $? -ne 0 ]; then
  exit 1
fi

poetry run ruff check
if [ $? -ne 0 ]; then
  exit 1
fi

poetry run pyright
if [ $? -ne 0 ]; then
  exit 1
fi

poetry run pytest -m "not integration"
if [ $? -ne 0 ]; then
  exit 1
fi

poetry build