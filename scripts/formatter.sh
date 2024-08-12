#!/bin/sh -e
set -x

ruff check fastapi_kafka tests --fix
ruff format fastapi_kafka tests
