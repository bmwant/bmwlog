#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR=$(dirname "${DIR}")

echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
TAG=$(sha1sum poetry.lock | awk '{ print $1 }')
echo "Current tag is ${TAG}"
IMAGE_NAME="bmwant/bmwlog:${TAG}"
docker push ${IMAGE_NAME}
# Retag image as latest
LATEST_IMAGE_NAME="bmwant/bmwlog:latest"
docker tag ${IMAGE_NAME} ${LATEST_IMAGE_NAME}
docker push ${LATEST_IMAGE_NAME}
