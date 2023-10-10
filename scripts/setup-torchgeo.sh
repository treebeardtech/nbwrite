#! /usr/bin/env bash

set -e -u -o pipefail

cd "$(dirname "$0")/.."

cd tests/resources
poetry install