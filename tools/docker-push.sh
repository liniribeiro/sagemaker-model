#!/usr/bin/env bash

set -e
SERVICE_NAME_VERSION="aliniribeiroo/sagemaker-model:dev"
docker tag model $SERVICE_NAME_VERSION
docker push $SERVICE_NAME_VERSION

