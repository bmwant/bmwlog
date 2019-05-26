#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR=$(dirname "${DIR}")

source "${DIR}/common.sh"

echo "Root directory is ${ROOT_DIR}"
pushd "${ROOT_DIR}"
  echo "Getting current app image tag"
  TAG=$(get_current_tag)
  IMAGE_NAME="bmwant/bmwlog:${TAG}"
  echo -e "Current tag: ${TAG}\nImage: ${IMAGE_NAME}"

  NOT_PRESENT=$(check_image_exists ${IMAGE_NAME})
  if [[ ${NOT_PRESENT} -eq 0 ]]; then
    echo "Image already exists, skipping build"
    exit 0
  fi

  echo "Building app docker image"
  COMMIT_SHA=$(git rev-parse HEAD)
  docker build -t ${IMAGE_NAME} --label "commit=${COMMIT_SHA}" .
popd
