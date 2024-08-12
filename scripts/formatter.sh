#!/bin/sh -e
set -x

pip install -r requirements.txt
ruff check fastapi_kafka tests --fix
ruff format fastapi_kafka tests
