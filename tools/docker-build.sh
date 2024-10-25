#!/usr/bin/env bash

set -e


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_DIR=$(realpath "${SCRIPT_DIR}/../")

docker buildx build -t model $PROJECT_DIR

