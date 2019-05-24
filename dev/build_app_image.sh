#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR=$(dirname "${DIR}")

echo "Root directory is ${ROOT_DIR}"

function check_image_exists() {
  # Try to pull image provided as argument
  # Allow command to fail
  # Suppress any output to stdout/stderr
  # Print exit code. Zero exit code means that the image exists
  set +e
  docker pull $1 > /dev/null 2>&1
  local rc=$?
  set -e

  echo ${rc}
}

pushd "${ROOT_DIR}"
  echo "Getting current tag for worker image"
  TAG=$(sha1sum poetry.lock | awk '{ print $1 }')
  echo "Current tag is ${TAG}"
  IMAGE_NAME="bmwant/bmwlog:${TAG}"

  NOT_PRESENT=$(check_image_exists ${IMAGE_NAME})
  if [[ ${NOT_PRESENT} -eq 0 ]]; then
    note "Image already exists, skipping build"
    exit 0
  fi

  echo "Building app docker image"
  docker build -t ${IMAGE_NAME} .
popd
